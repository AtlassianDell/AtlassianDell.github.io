import math

def handle_amath(self, parts):
    current_line_num = self.state.instruction_pointer + 1
    if len(parts) >= 3:
        op = parts[1].upper()
        dest = parts[2]
        args = [self.state.get_value(arg) for arg in parts[3:]]
        result = None
        try:
            if op == "SIN" and len(args) == 1:
                result = math.sin(args[0])
            elif op == "COS" and len(args) == 1:
                result = math.cos(args[0])
            elif op == "TAN" and len(args) == 1:
                result = math.tan(args[0])
            elif op == "ASIN" and len(args) == 1:
                result = math.asin(args[0])
            elif op == "ACOS" and len(args) == 1:
                result = math.acos(args[0])
            elif op == "ATAN" and len(args) == 1:
                result = math.atan(args[0])
            elif op == "ATAN2" and len(args) == 2:
                result = math.atan2(args[0], args[1])
            elif op == "LOG" and len(args) == 1:
                if args[0] > 0:
                    result = math.log(args[0])
                else:
                    raise VertigoValueError("Logarithm of non-positive number.", line_num=current_line_num)
            elif op == "LOG10" and len(args) == 1:
                if args[0] > 0:
                    result = math.log10(args[0])
                else:
                    raise VertigoValueError("Logarithm of non-positive number.", line_num=current_line_num)
            elif op == "EXP" and len(args) == 1:
                result = math.exp(args[0])
            elif op == "SQRT" and len(args) == 1:
                if args[0] >= 0:
                    result = math.sqrt(args[0])
                else:
                    raise VertigoValueError("Square root of negative number.", line_num=current_line_num)
            elif op == "ABS" and len(args) == 1:
                result = abs(args[0])
            elif op == "FLOOR" and len(args) == 1:
                result = math.floor(args[0])
            elif op == "CEIL" and len(args) == 1:
                result = math.ceil(args[0])
            elif op == "GCD" and len(args) == 2:
                try:
                    result = math.gcd(int(args[0]), int(args[1]))
                except TypeError:
                    raise VertigoTypeError("GCD requires integer arguments.", line_num=current_line_num)
            elif op == "LCM" and len(args) == 2:
                try:
                    num1, num2 = int(args[0]), int(args[1])
                    if num1 == 0 or num2 == 0:
                        result = 0
                    else:
                        result = abs(num1 * num2) // math.gcd(num1, num2)
                except TypeError:
                    raise VertigoTypeError("LCM requires integer arguments.", line_num=current_line_num)
                except ZeroDivisionError:
                    raise VertigoZeroDivisionError("LCM calculation error due to zero argument.", line_num=current_line_num)
            elif op == "ROUND" and len(args) in [1, 2]:
                if len(args) == 1:
                    result = round(args[0])
                else:
                    try:
                        result = round(args[0], int(args[1]))
                    except TypeError:
                        raise VertigoTypeError("ROUND decimal places must be an integer.", line_num=current_line_num)
            elif op == "FACTORIAL" and len(args) == 1:
                if isinstance(args[0], int) and args[0] >= 0:
                    result = math.factorial(args[0])
                else:
                    raise VertigoValueError("FACTORIAL requires a non-negative integer.", line_num=current_line_num)
            elif op == "COMPLEX" and len(args) == 2:
                result = complex(args[0], args[1])
            elif op == "REALPART" and len(args) == 1:
                if not isinstance(args[0], complex):
                    raise VertigoTypeError("REALPART requires a complex number.", line_num=current_line_num)
                result = args[0].real
            elif op == "IMAGPART" and len(args) == 1:
                if not isinstance(args[0], complex):
                    raise VertigoTypeError("IMAGPART requires a complex number.", line_num=current_line_num)
                result = args[0].imag
            elif op == "CONJUGATE" and len(args) == 1:
                if not isinstance(args[0], complex):
                    raise VertigoTypeError("CONJUGATE requires a complex number.", line_num=current_line_num)
                result = args[0].conjugate()
            elif op == "MAGNITUDE" and len(args) == 1:
                if not isinstance(args[0], complex):
                    raise VertigoTypeError("MAGNITUDE requires a complex number.", line_num=current_line_num)
                result = abs(args[0])
            elif op == "PHASE" and len(args) == 1:
                if not isinstance(args[0], complex):
                    raise VertigoTypeError("PHASE requires a complex number.", line_num=current_line_num)
                result = math.atan2(args[0].imag, args[0].real)
            else:
                raise VertigoSyntaxError(f"Unknown AMATH operation '{op}' or incorrect number/types of arguments.", line_num=current_line_num)
            if result is not None:
                if dest == "&":
                    if not self.state.current_stack_name:
                        raise VertigoLookupError("No stack selected for '&' destination.", line_num=current_line_num)
                    self.state.stacks[self.state.current_stack_name].append(result)
                elif dest in self.state.registers:
                    self.state.registers[dest] = result
                elif dest.startswith("+"):
                    raise VertigoTypeError(f"Cannot assign to immutable '{dest}'.", line_num=current_line_num)
                else:
                    raise VertigoNameError(f"Invalid destination '{dest}'. Must be a register or '&'.", line_num=current_line_num)
        except (ValueError, TypeError) as e:
            raise VertigoRuntimeError(f"Math operation '{op}' failed: {e}", line_num=current_line_num)
        except Exception as e:
            raise VertigoRuntimeError(f"An unexpected error occurred during AMATH operation '{op}': {e}", line_num=current_line_num)
    else:
        raise VertigoSyntaxError("Invalid AMATH syntax. Expected 'AMATH <operation> <destination> [arg1] [arg2...]'.", line_num=current_line_num)

def _initialize_amath_library(interpreter_state):
    interpreter_state.immutables["+pi"] = 3.14159
    interpreter_state.immutables["+e"] = 2.71828
    interpreter_state.immutables["+y"] = 0.57721
    interpreter_state.immutables["+gr"] = 1.618
    interpreter_state.immutables["+c"] = 299792458
    interpreter_state.immutables["+g"] = 6.6743e-11
    interpreter_state.immutables["+h"] = 1.054571817e-34

# This special global dictionary exports the library's components to Vertigo
__vertigo_library__ = {
    "instructions": {"AMATH": handle_amath},
    "initializer": _initialize_amath_library
}
