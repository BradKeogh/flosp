


def test_flosp_import():
    "check import of flosp."
    print('start import test script.')
    import flosp
    
    print('end import test script.')
    
    return('flosp' in dir())


def test_interface_import():
    "check can import Interface class with relative path."
    from ..interface import Interface
    return('Interface' in dir() )
