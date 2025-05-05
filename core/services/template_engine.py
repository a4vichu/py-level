import re
from typing import Any, Dict, List, Optional, Union
from html.parser import HTMLParser
from datetime import datetime
import json
import math
import random
import string
import itertools
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import hashlib
import uuid

from core.facade.config import Config
from core.facade.env import Env
from core.facade.app import App
from core.facade.path import Path
from core.facade.log import Log
from core.facade.url import Url
from core.facade.redirect import Redirect
from core.facade.request import Request
from core.facade.translation import Translation
from core.facade.collection import Collection
from core.facade.security import Security
from core.facade.event import Event
from core.facade.asset import Asset

class TemplateEngine:
    def __init__(self):
        # Initialize asset facade
        self._asset = Asset()
        
        # Simpler, more robust patterns
        self.interpolation_pattern = re.compile(r'\{\{\s*(.*?)\s*\}\}')
        self.p_if_pattern = re.compile(r'<(\w+)([^>]*?)\s+p-if=["\']([^"\']*)["\']([^>]*?)>(.*?)</\1>', re.DOTALL | re.IGNORECASE)
        self.p_for_pattern = re.compile(r'<(\w+)([^>]*?)\s+p-for=["\']([^"\']*?)\s+in\s+([^"\']*?)["\']([^>]*?)>(.*?)</\1>', re.DOTALL | re.IGNORECASE)
        self.p_bind_pattern = re.compile(r'p-bind:(\w+)=["\']([^"\']*)["\']', re.IGNORECASE)
        
        # Helper patterns
        self.helper_patterns = {
            'config': re.compile(r'config\(([^)]+)\)'),
            'env': re.compile(r'env\(([^)]+)\)'),
            'app': re.compile(r'app\(([^)]+)\)'),
            'base_path': re.compile(r'base_path\(\)'),
            'app_path': re.compile(r'app_path\(\)'),
            'config_path': re.compile(r'config_path\(\)'),
            'database_path': re.compile(r'database_path\(\)'),
            'resource_path': re.compile(r'resource_path\(\)'),
            'storage_path': re.compile(r'storage_path\(\)'),
            'asset': re.compile(r'asset\(([^)]+)\)'),
            'url': re.compile(r'url\(([^)]+)\)'),
            'secure_asset': re.compile(r'secure_asset\(([^)]+)\)'),
            'secure_url': re.compile(r'secure_url\(([^)]+)\)'),
            'route': re.compile(r'route\(([^)]+)\)'),
            'redirect': re.compile(r'redirect\(([^)]+)\)'),
            'back': re.compile(r'back\(\)'),
            'request': re.compile(r'request\(\)'),
            'old': re.compile(r'old\(([^)]+)\)'),
            'session': re.compile(r'session\(([^)]+)\)'),
            '__': re.compile(r'__\(([^)]+)\)'),
            'trans': re.compile(r'trans\(([^)]+)\)'),
            'trans_choice': re.compile(r'trans_choice\(([^)]+)\)'),
            'collect': re.compile(r'collect\(([^)]+)\)'),
            'data_get': re.compile(r'data_get\(([^)]+)\)'),
            'data_set': re.compile(r'data_set\(([^)]+)\)'),
            'head': re.compile(r'head\(([^)]+)\)'),
            'last': re.compile(r'last\(([^)]+)\)'),
            'value': re.compile(r'value\(([^)]+)\)'),
            'with_value': re.compile(r'with_value\(([^)]+)\)'),
            'bcrypt_hash': re.compile(r'bcrypt_hash\(([^)]+)\)'),
            'bcrypt_check': re.compile(r'bcrypt_check\(([^)]+)\)'),
            'event': re.compile(r'event\(([^)]+)\)'),
            'dispatch': re.compile(r'dispatch\(([^)]+)\)')
        }

        # Add template functions
        self.template_functions = {
            # String functions
            'upper': str.upper,
            'lower': str.lower,
            'capitalize': str.capitalize,
            'title': str.title,
            'trim': str.strip,
            'ltrim': str.lstrip,
            'rtrim': str.rstrip,
            'length': len,
            'substr': lambda s, start, length=None: s[start:start + length] if length else s[start:],
            'replace': str.replace,
            'split': str.split,
            'join': lambda arr, sep='': sep.join(arr),
            'concat': lambda *args: ''.join(str(arg) for arg in args),
            'pad': lambda s, length, char=' ': s.ljust(length, char),
            'pad_left': lambda s, length, char=' ': s.rjust(length, char),
            'pad_right': lambda s, length, char=' ': s.ljust(length, char),
            'repeat': lambda s, times: s * times,
            'slugify': lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-'),
            'nl2br': lambda s: s.replace('\n', '<br>'),
            'escape': lambda s: str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'),
            'raw': lambda x: x,

            # Number functions
            'round': round,
            'floor': math.floor,
            'ceil': math.ceil,
            'abs': abs,
            'min': min,
            'max': max,
            'sum': sum,
            'random': random.random,
            'random_int': random.randint,
            'format_number': lambda n, decimals=2: format(float(n), f'.{decimals}f'),
            'format_currency': lambda n, symbol='$', decimals=2: f"{symbol}{format(float(n), f'.{decimals}f')}",
            'format_percent': lambda n, decimals=2: f"{format(float(n) * 100, f'.{decimals}f')}%",

            # Array functions
            'first': lambda arr: arr[0] if arr else None,
            'last': lambda arr: arr[-1] if arr else None,
            'slice': lambda arr, start, end=None: arr[start:end],
            'reverse': lambda arr: list(reversed(arr)),
            'sort': sorted,
            'shuffle': lambda arr: random.sample(arr, len(arr)),
            'unique': lambda arr: list(dict.fromkeys(arr)),
            'count': len,
            'in_array': lambda item, arr: item in arr,
            'pluck': lambda arr, key: [item.get(key) for item in arr if isinstance(item, dict)],
            'group_by': lambda arr, key: {k: list(g) for k, g in itertools.groupby(sorted(arr, key=lambda x: x.get(key)), key=lambda x: x.get(key))},
            'chunk': lambda arr, size: [arr[i:i + size] for i in range(0, len(arr), size)],

            # Object functions
            'keys': dict.keys,
            'values': dict.values,
            'items': dict.items,
            'get': lambda obj, key, default=None: obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default),
            'has': lambda obj, key: key in obj if isinstance(obj, dict) else hasattr(obj, key),
            'merge': lambda *dicts: {k: v for d in dicts for k, v in d.items()},
            'pick': lambda obj, *keys: {k: obj[k] for k in keys if k in obj},
            'omit': lambda obj, *keys: {k: v for k, v in obj.items() if k not in keys},

            # Date functions
            'now': datetime.now,
            'date': lambda fmt='%Y-%m-%d': datetime.now().strftime(fmt),
            'time': lambda fmt='%H:%M:%S': datetime.now().strftime(fmt),
            'datetime': lambda fmt='%Y-%m-%d %H:%M:%S': datetime.now().strftime(fmt),
            'format_date': lambda date, fmt='%Y-%m-%d': date.strftime(fmt) if isinstance(date, datetime) else date,
            'add_days': lambda date, days: date + timedelta(days=days) if isinstance(date, datetime) else date,
            'add_months': lambda date, months: date + relativedelta(months=months) if isinstance(date, datetime) else date,
            'add_years': lambda date, years: date + relativedelta(years=years) if isinstance(date, datetime) else date,
            'diff_days': lambda date1, date2: (date2 - date1).days if isinstance(date1, datetime) and isinstance(date2, datetime) else 0,

            # JSON functions
            'json_encode': json.dumps,
            'json_decode': json.loads,
            'to_json': json.dumps,
            'from_json': json.loads,

            # Math functions
            'add': lambda x, y: float(x) + float(y),
            'subtract': lambda x, y: float(x) - float(y),
            'multiply': lambda x, y: float(x) * float(y),
            'divide': lambda x, y: float(x) / float(y) if float(y) != 0 else 0,
            'modulo': lambda x, y: float(x) % float(y) if float(y) != 0 else 0,
            'power': lambda x, y: float(x) ** float(y),
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e,

            # Boolean functions
            'is_empty': lambda x: not bool(x),
            'is_not_empty': lambda x: bool(x),
            'is_null': lambda x: x is None,
            'is_not_null': lambda x: x is not None,
            'is_numeric': lambda x: str(x).replace('.', '', 1).isdigit(),
            'is_string': lambda x: isinstance(x, str),
            'is_array': lambda x: isinstance(x, (list, tuple)),
            'is_object': lambda x: isinstance(x, dict),
            'is_date': lambda x: isinstance(x, datetime),
            'is_boolean': lambda x: isinstance(x, bool),
            'is_true': lambda x: bool(x) is True,
            'is_false': lambda x: bool(x) is False,

            # Conditional functions
            'default': lambda x, default: x if x is not None and x != '' else default,
            'ternary': lambda condition, true_value, false_value: true_value if condition else false_value,
            'coalesce': lambda *args: next((arg for arg in args if arg is not None and arg != ''), None),

            # String generation
            'random_string': lambda length=10: ''.join(random.choices(string.ascii_letters + string.digits, k=length)),
            'uuid': lambda: str(uuid.uuid4()),
            'md5': lambda s: hashlib.md5(str(s).encode()).hexdigest(),
            'sha1': lambda s: hashlib.sha1(str(s).encode()).hexdigest(),
            'sha256': lambda s: hashlib.sha256(str(s).encode()).hexdigest(),

            # Array generation
            'range': range,
            'repeat': lambda item, times: [item] * times,
            'sequence': lambda start, end, step=1: list(range(start, end + 1, step)),

            # Object generation
            'object': lambda **kwargs: kwargs,
            'array': lambda *args: list(args),
            'set': lambda *args: set(args),
            'tuple': lambda *args: tuple(args),

            # Utility functions
            'dump': lambda x: print(x) or x,  # For debugging
            'debug': lambda x: f"<!-- Debug: {x} -->",  # For debugging in HTML
            'type': type,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,

            # Helper functions
            'config': lambda key, default=None: Config.get(key, default),
            'env': lambda key, default=None: Env.get(key, default),
            'app': lambda key, default=None: App.get(key, default),
            'base_path': Path.base,
            'app_path': Path.app,
            'config_path': Path.config,
            'database_path': Path.database,
            'resource_path': Path.resource,
            'storage_path': Path.storage,
            'asset': lambda path: Url.asset(path),
            'url': lambda path, parameters=None: Url.to(path, parameters),
            'secure_asset': lambda path: Url.secure_asset(path),
            'secure_url': lambda path, parameters=None: Url.secure(path, parameters),
            'route': lambda name, parameters=None: Url.route(name, parameters),
            'redirect': lambda path, parameters=None: Redirect.to(path, parameters),
            'back': Redirect.back,
            'request': lambda key=None, default=None: Request.get(key, default),
            'old': lambda key=None, default=None: Request.old(key, default),
            'session': lambda key=None, default=None: Request.session(key, default),
            '__': lambda key, parameters=None: Translation.get(key, parameters),
            'trans': lambda key, parameters=None: Translation.get(key, parameters),
            'trans_choice': lambda key, number, parameters=None: Translation.choice(key, number, parameters),
            'collect': Collection.make,
            'data_get': Collection.get,
            'data_set': Collection.set,
            'head': Collection.head,
            'last': Collection.last,
            'value': Collection.value,
            'with_value': Collection.with_value,
            'bcrypt_hash': Security.hash,
            'bcrypt_check': Security.check,
            'event': Event.listen,
            'dispatch': Event.dispatch
        }

    @property
    def asset(self) -> Asset:
        """Get the asset facade instance."""
        return self._asset

    def render(self, template: str, context: Dict[str, Any]) -> str:
        """Render the template with the given context."""
        try:
            # First, process all nested structures
            processed = template
            while True:
                # Keep track of changes
                old_processed = processed
                
                # Process loops first (can be nested)
                processed = self._process_loops(processed, context)
                
                # Then process conditionals
                processed = self._process_conditionals(processed, context)
                
                # Process p-bind attributes
                processed = self._process_bindings(processed, context)
                
                # If no changes were made, we're done
                if old_processed == processed:
                    break
            
            # Finally process interpolations
            processed = self._process_interpolations(processed, context)
            
            return processed
        except Exception as e:
            return f"<!-- Template Error: {str(e)} -->"

    def _get_value_from_context(self, key: str, context: Dict[str, Any]) -> Any:
        """Get a value from the context using dot notation."""
        try:
            # Handle direct variable access first
            key = key.strip()
            if key in context:
                return context[key]

            # Handle dot notation
            current = context
            for part in key.split('.'):
                part = part.strip()
                if isinstance(current, dict):
                    if part not in current:
                        return None
                    current = current[part]
                elif hasattr(current, part):
                    # Handle attribute access
                    current = getattr(current, part)
                else:
                    return None
            return current
        except Exception:
            return None

    def _process_interpolations(self, template: str, context: Dict[str, Any]) -> str:
        """Process all {{ expression }} interpolations in the template."""
        def replace_interpolation(match):
            expression = match.group(1).strip()
            result = self._eval_expression(expression, context)
            return str(result) if result is not None else ""
        
        return self.interpolation_pattern.sub(replace_interpolation, template)
    
    def _process_conditionals(self, template: str, context: Dict[str, Any]) -> str:
        """Process all p-if conditionals in the template."""
        def replace_conditional(match):
            tag, pre_attrs, condition, post_attrs, content = match.groups()
            
            # Remove p-if attribute for the final output
            attrs = pre_attrs.replace(f'p-if="{condition}"', '') if pre_attrs else ''
            attrs += post_attrs if post_attrs else ''
            attrs = attrs.strip()
            attrs = f" {attrs}" if attrs else ""
            
            # Evaluate the condition
            result = self._eval_expression(condition, context)
            
            if result:
                # If condition is true, render the content with the same context
                rendered_content = self.render(content, context)
                return f"<{tag}{attrs}>{rendered_content}</{tag}>"
            return ""
        
        return self.p_if_pattern.sub(replace_conditional, template)
    
    def _process_loops(self, template: str, context: Dict[str, Any]) -> str:
        """Process all p-for loops in the template."""
        def replace_loop(match):
            tag, pre_attrs, item_var, items_expr, post_attrs, content = match.groups()
            
            # Remove p-for attribute for the final output
            p_for_attr = f'p-for="{item_var} in {items_expr}"'
            attrs = pre_attrs.replace(p_for_attr, '') if pre_attrs else ''
            attrs += post_attrs if post_attrs else ''
            attrs = attrs.strip()
            attrs = f" {attrs}" if attrs else ""
            
            try:
                # Get the items to iterate over
                items = self._get_value_from_context(items_expr, context)
                if not items or not isinstance(items, (list, tuple, dict)):
                    return ""
                
                # Render the content for each item
                result = []
                for item in items:
                    # Create a new context for this iteration
                    loop_context = dict(context)
                    loop_context[item_var] = item
                    
                    # Render the content with the loop context
                    rendered_content = self.render(content, loop_context)
                    result.append(f"<{tag}{attrs}>{rendered_content}</{tag}>")
                
                return "".join(result)
            except Exception as e:
                return f"<!-- Loop error: {str(e)} -->"
        
        return self.p_for_pattern.sub(replace_loop, template)

    def _process_bindings(self, template: str, context: Dict[str, Any]) -> str:
        """Process all p-bind attributes in the template."""
        def replace_binding(match):
            attr_name, expr = match.groups()
            value = self._eval_expression(expr, context)
            if value is not None:
                return f'{attr_name}="{value}"'
            return ''
        
        return self.p_bind_pattern.sub(replace_binding, template)

    def _eval_expression(self, expression: str, context: Dict[str, Any]) -> Any:
        """Safely evaluate an expression in the given context, supporting JS-like syntax and dot notation for dicts."""
        try:
            # --- JS-like to Python translation ---
            expr = expression.strip()

            # Handle function calls
            if '(' in expr:
                # Extract function name and arguments
                func_match = re.match(r'(\w+)\((.*)\)', expr)
                if func_match:
                    func_name = func_match.group(1)
                    args_str = func_match.group(2)
                    
                    # Parse arguments
                    args = []
                    current_arg = ''
                    in_string = False
                    string_char = None
                    bracket_count = 0
                    
                    for char in args_str:
                        if char in ['"', "'"] and (not in_string or char == string_char):
                            in_string = not in_string
                            string_char = char if in_string else None
                            current_arg += char
                        elif char == ',' and not in_string and bracket_count == 0:
                            args.append(current_arg.strip())
                            current_arg = ''
                        else:
                            if char in ['(', '[']:
                                bracket_count += 1
                            elif char in [')', ']']:
                                bracket_count -= 1
                            current_arg += char
                    
                    if current_arg:
                        args.append(current_arg.strip())
                    
                    # Evaluate arguments
                    eval_args = [self._eval_expression(arg, context) for arg in args]
                    
                    # Call the function
                    if func_name in self.template_functions:
                        return self.template_functions[func_name](*eval_args)
                    elif func_name in context:
                        func = context[func_name]
                        if callable(func):
                            return func(*eval_args)
                    return None

            # Ternary: a ? b : c  -->  (b if a else c)
            if '?' in expr and ':' in expr:
                q_idx = expr.find('?')
                c_idx = expr.find(':', q_idx)
                cond = expr[:q_idx].strip()
                true_val = expr[q_idx+1:c_idx].strip()
                false_val = expr[c_idx+1:].strip()
                expr = f'({true_val}) if ({cond}) else ({false_val})'

            # Nullish coalescing: a ?? b  -->  a if a is not None else b
            if '??' in expr:
                parts = [p.strip() for p in expr.split('??', 1)]
                expr = f'({parts[0]}) if ({parts[0]}) is not None else ({parts[1]})'

            # .toFixed(n): x.toFixed(2) --> format(x, '.2f')
            tofixed_match = re.search(r'([\w\.]+)\.toFixed\((\d)\)', expr)
            if tofixed_match:
                var = tofixed_match.group(1)
                digits = tofixed_match.group(2)
                expr = re.sub(r'([\w\.]+)\.toFixed\((\d)\)', f"format(\1, '.{digits}f')", expr)

            # Replace JS-style '&&' and '||' with Python 'and'/'or'
            expr = expr.replace('&&', ' and ').replace('||', ' or ')

            # --- Dot notation to dict access ---
            def dot_to_dict_access(e):
                # Only replace for known context keys (like 'product')
                for key in context.keys():
                    # Replace key.something with key['something']
                    e = re.sub(rf'\b{key}\.([a-zA-Z_][\w]*)', rf"{key}['\1']", e)
                return e
            expr = dot_to_dict_access(expr)

            # Allow context variables in eval
            safe_builtins = {'format': format, 'str': str, 'int': int, 'float': float, 'bool': bool, 'len': len}
            eval_context = dict(safe_builtins)
            eval_context.update(context)
            eval_context.update(self.template_functions)

            # Try to eval as Python
            result = eval(expr, {"__builtins__": {}}, eval_context)
            return result
        except Exception as e:
            # Fallback to simple variable access
            return self._get_value_from_context(expression, context)

    def safe_to_fixed(self, val, digits):
        try:
            return format(float(val or 0), f'.{digits}f')
        except Exception:
            return '0.00'

class Template:
    def __init__(self, template_string: str):
        self.template_string = template_string
        self.engine = TemplateEngine()
    
    def render(self, context: Dict[str, Any]) -> str:
        """Render the template with the given context."""
        return self.engine.render(self.template_string, context) 