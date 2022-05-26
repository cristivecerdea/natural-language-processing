# natural-language-processing
sorry for not refactoring the code :(


contains 2 projects:


  -attribute generator:
  
  		-you should add a folder containing xml files to transform in word vectors
  
  		-this project eliminates all punctuation and numbers from text and extracts the root of the word using snowball stemmer
        
		-generates frequency_vectors.txt file which contains the attribute list and frequency vector (using some type of ARFF)


-nlp-interrogation: 

		-you add the frequency_vectors.txt file generated from before

		-run the project to normalize the vectors using nominal normalization and invers term frequency
        
		-after the normalization you can introduce the interrogation in interrogation.txt file, save it, and press space in the console
        
		-generates normalized version for interrogation and calculates cosine similarity displaing the name of the top 10 most relevant documents
         
		 
maybe will do in the future:  
		
		-refactor code
        
		-add information gain for attributes
        
		-optimize code
        
		-implement processing of more type of documents
