import string

print()
language = input("Lista de idiomas:\n\t[1]Inglês\n\t[2]Português\nEscolha um numero para jogar: ")

if(int(language)==1):
	#carrega arquivo de palavras
	wordsFile = open("english-words.txt","r")
if(int(language)==2):
	#carrega arquivo de palavras
	wordsFile = open("ptbr-words.txt","r")


wordsList = wordsFile.read().splitlines()
#mantem somente as palavras de 5 caracteres
wordsList[:] = [word.lower() for word in wordsList if len(word)==5 and word.isalpha()]

#iniciando globais
command = ""
correctWord = ["?"]*5
bannedChars = []
mandatoryChars = []
closeNumber = 20

def removeGuessesByRightPosition(letter, position):
	wordsList[:] = [word for word in wordsList if word[position-1]==letter]

def removeGuessesByUnknowPosition(letter, position):
	wordsList[:] = [word for word in wordsList if letter in word and not word[position-1]==letter ]

def removeLetterFromGuesses(letter):
	wordsList[:] = [word for word in wordsList if not letter in word]
	pass

def showCommandList():
	print("""
	Lista de comandos do programa:
	\t> !\t define uma letra em uma posição específica [exemplo: '>! a 2' - letra a na posição 2]
	\t> ?\t define uma letra em uma posição desconhecida [exemplo: '>? b 4' - letra b esta na palavra, mas não se sabe a posição correta, apenas que não é a posição 4]
	\t> x\t exclui todos os palpites que possuem uma letra [exemplo: '>x a' - exclui todas as palavras que possuem a letra a]
	\t> word\t mostra a completude da palavra atual com os caracteres de posicao correta descobertos
	\t> all\t mostra todas as palavras possiveis
	\t> alert\t altera o numero de alerta de proximidade da resposta (padrão: 20) [exemplo: '>alert 10' - quando a lista de palavras for inferior a 10, o alerta é exibido]
	\t> exit\t encerrar programa
	""")
	pass

def letterOnPosition(letter, position):
	correctWord[int(position) - 1] = letter
	removeGuessesByRightPosition(letter,position)
	mandatoryChars.append(letter)
	closeInfo()
	pass

def letterOnUnknowPosition(letter, position):
	mandatoryChars.append(letter)
	removeGuessesByUnknowPosition(letter, position)
	closeInfo()
	pass

def banLetter(letter):
	bannedChars.append(letter)
	removeLetterFromGuesses(letter)
	closeInfo()
	pass

def showCurrentWord():
	print (" ".join(correctWord))
	closeInfo()
	pass

def showAllWords():
	print(wordsList)
	print ("\tExistem %s palavras na lista..." % len(wordsList))

def closeInfo():
	if len(wordsList) == 1:
		print("\tDe acordo com seus comandos, somente uma palavra do nosso dicionario é possível: %s" % (wordsList[0]))
		exit()
	if len(wordsList) <= closeNumber:
		print("\t Existem %s palavras dentre as possíveis. Digite o comando 'all' para vê-las!" % (len(wordsList)))
	return

def getFrequency():
	frequency = dict.fromkeys(string.ascii_lowercase, 0)
	for word in wordsList:
		temp = "".join(set(word))
		for letter in temp:
			frequency[letter]+=1
	return frequency

def getWordsPoints(frequency):
	wordsPoints = dict.fromkeys(wordsList,0)
	for word in wordsList:
		for letter in word:
			wordsPoints[word]+=frequency[letter]
	return wordsPoints

def printWordPoints():
	wordsPoints = getWordsPoints(getFrequency())
	print(wordsPoints)
	print({k: v for k, v in sorted(wordsPoints.items(), key=lambda item: item[1])})


while(command != "exit"):
	command = input("Digite o comando (para lista de comandos digite help): ")
	command = command.lower()

	if (command == "exit"):
		continue
	
	if (command =="help"):
		showCommandList()
		continue

	if (command =="all"):
		showAllWords()
		continue

	if (command == "word"):
		showCurrentWord()
		continue
	
	if (command[0]=="!"):
		args = command.split(" ")
		letterOnPosition(args[1],int(args[2]))
		continue
	
	if (command[0]=="?"):
		args = command.split(" ")
		letterOnUnknowPosition(args[1], int(args[2]))
		continue

	if (command[0]=="x"):
		args = command.split(" ")
		banLetter(args[1])
		continue
	
	if (command[0]=="%"):
		printWordPoints()
		continue

