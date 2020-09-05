import pymongo

def insert(condition, diagnosis):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['Doctor']
    mycol = mydb['Morning Shift']
    d = {"Condition":condition, "Diagnosis":diagnosis}
    mycol.insert_one(d)
    myclient.close()

def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    #client = vision.ImageAnnotatorClient()
    client = vision.ImageAnnotatorClient.from_service_account_json("apikey.json")
    file_object = open('prescription.txt', 'a')
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))
                    file_object.write(word_text)
                    file_object.write(' ')
                    #for symbol in word.symbols:
                        #print('\tSymbol: {} (confidence: {})'.format(
                            #symbol.text, symbol.confidence))
                file_object.write('\n')
            file_object.write('\n')

    file_object.close()
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(response.error.message))
        
        return
    
def split_diag_condition():
    import io
    file_object = open('prescription.txt', 'r')

    f1 = open('cond-PA.txt', 'w')
    f2 = open('diag-PA.txt', 'w')

    str = file_object.read()
    li = str.rsplit("Diagnosis:", 1)

    f1.write(li[0])
    
    d = 'Diagnosis:'+li[1]
    f2.write(d)

    file_object.close()
    f1.close()
    f2.close()
    insert(li[0], li[1])
    
    return 

detect_document('PA.jpeg')
split_diag_condition()

