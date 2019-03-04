from flosp import Interface 

H = Interface("./example/setup.py")
# a = interface.flosp_class()

H.load_dataED('./example/example_data.csv')

print(H.data.ED.head(1))
# print(H.data)
# print(H.metadata.SETUP_FILE_PATH)
print()
#print(H.metadata.EDdataRAW_expected_cols)