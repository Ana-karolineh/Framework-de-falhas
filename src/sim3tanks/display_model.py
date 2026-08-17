def display_model(self, struct_var=None, _prefix1='+-- ', _prefix2='O-- '):
    from .sim3tanks import Struct
    if struct_var is None:
        struct_var = self.Model
    is_there_subfield = False
    for key, value in struct_var.__dict__.items():
        if isinstance(value, Struct):
            is_there_subfield = True
            print(f'\n{_prefix1}{key} (Struct)')
            display_model(self, value, _prefix1, _prefix2)
        elif is_there_subfield:
            print(f'\n{_prefix1}{key}: {value} ({type(value).__name__})')
        else:
            print(f'\t{_prefix2}{key}: {value} ({type(value).__name__})')
