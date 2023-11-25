import json
class General():
    def prettyPrint(self, dictionary):
        print("[ TYPE OF PRETTY PRINT ] ",type(dict), isinstance(dictionary,object))
        if dictionary is None:
            return
        if type(dictionary) is not dict:
            print(dictionary)
            return
        if isinstance(dictionary,object):
            print(json.dumps(
                dictionary.dict(),
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            ))
            return
        if type(dictionary) is dict:
            print(json.dumps(
                dictionary,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            ))
            return
 