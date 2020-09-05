# Multilingual-Prescription-Reader

Tried and tested various different OCR engines, first a lightweight Tesseract, then, Google Vision's Text Detection and then finally Vision's Document Text Detection API. The latter worked best for handwritten text while Tesseract worked well with text in the Wild. 
From the OCR engine's output, I then parsed the document contents into Diagnosis and Prescription, and wrote these separately into a MongoDB database using the PyMongo driver. Tested with various prescriptions written in English and Hindi.
