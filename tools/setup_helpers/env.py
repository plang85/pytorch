import os


def check_env_flag(name):
    return os.getenv(name, '').upper() in ['ON', '1', 'YES', 'TRUE', 'Y']


class SanitizerFlags:

    def __init__(self):
        self.flags = []

    def add_to(self, compiler_flags, linker_flags):
        compiler_flags += self.flags
        linker_flags += self.flags
        return compiler_flags, linker_flags
    
    @classmethod
    def from_env(cls, env=None):
        """
        Detects flags from environment variables, e.g.
        SANITIZE=thread,undefined
        """
        if not env:
            env = os.environ.copy()
        sanitizers = env.get('SANITIZE', '')
        sanitizer_flags = cls()
        if sanitizers:
            sanitizers = sanitizers.lower().split(',')
            for sanitizer in sanitizers:
                sanitizer_flags.flags.append('-fsanitize={}'.format(sanitizer))
        return sanitizer_flags
