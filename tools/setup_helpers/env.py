import os


def check_env_flag(name):
    return os.getenv(name, '').upper() in ['ON', '1', 'YES', 'TRUE', 'Y']


class SanitizerFlags:

    def __init__(self):
        self._flags = []

    def add_to_flags(self, compiler_flags, linker_flags):
        compiler_flags += self._flags
        linker_flags += self._flags
        return compiler_flags, linker_flags

    def add_to_env(self, var, env=None):
        if not env:
            env = os.environ
        if self.flags():
            env[var] = self.flags()

    def flags(self):
        return ' '.join(self._flags)
    
    @classmethod
    def from_env(cls, var, env=None):
        """
        Detects flags from environment variable, e.g.
        var=thread,undefined (comma separated).
        """
        if not env:
            env = os.environ.copy()
        sanitizers = env.get(var, '')
        sanitizer_flags = cls()
        if sanitizers:
            sanitizers = sanitizers.lower().split(',')
            for sanitizer in sanitizers:
                sanitizer_flags._flags.append('-fsanitize={}'.format(sanitizer))
        return sanitizer_flags
