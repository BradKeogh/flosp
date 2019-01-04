from flosp import Interface 

H = Interface("./example/setup.py")
# a = interface.flosp_class()

#h.load_data()

print(H.data)
print(H.metadata.setup_file_path)