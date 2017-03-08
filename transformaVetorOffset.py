#!/usr/bin/python

'''
	Comments - SOON
'''

import sys

try:
	file_in = str(sys.argv[1])
	file_out = str(sys.argv[2])
	arquivo_entrada = open(file_in, 'r')
	arquivo_saida = open(file_out, 'w')
except IndexError:
	print "Argumentos invalidos. Execute $python .py <arquivo de entrada> <arquivo de saida>"
	sys.exit()
	
# Variaveis para s7plc
nome_comunicacao = ("Testsystem:0","Testsystem_alarms:0")  #Edite aqui com os nomes configurados em s7plcConfigure. Index 0: Leitura. Index 1: Escrita. 
SCAN_field = '"I/O Intr"'
DTYP_field = '"S7plc"'

# Variaveis para logica
flag_transicao = 0
offset = [0]*2
numero_bits = [0]*2
tamanho_total = [0]*2
porta = [0,1] # Porta 0 significa leitura de dados do CLP. Porta 1 significa escrita de dados no CLP.
numeroLinha = 0
indiceVetorOffset = [0]*2
cat_da_variavel_antiga = ""
cat_da_variavel_atual = ""
tipo_da_variavel_antiga = ""
tipo_da_variavel_atual = ""

def escreve_cabecario(PLC_name):
	INP_field_cab = '"@%s"' %(PLC_name)	
	ZNAM_field = '"disconnected"'
	ONAM_field = '"connected"'
	ZSV_field = '"MAJOR"'
	DTYP_field_cab = '"S7plc stat"'
	FLNK_field = '"$(P)$(R)status-counter"'	
	bi_field = '"$(P)$(R)status"'
	arquivo_saida.write("record (bi, %s) {\n	field (DTYP, %s)\n	field (INP, %s)\n	field (SCAN, %s)\n	field (ZNAM, %s)\n	field (ONAM, %s)\n	field (ZSV, %s)\n	field(FLNK, %s)\n}\n" %(bi_field, DTYP_field_cab, INP_field_cab, SCAN_field, ZNAM_field, ONAM_field, ZSV_field, FLNK_field))
	
	CALC_field = '"A+1"'
	FNLK_field = '"$(P)$(R)disconnect-counter"'
	record_calc_field = '"$(P)$(R)status-counter"'
	INPA_field = '"$(P)$(R)status-counter"'
	arquivo_saida.write("record (calc, %s) {\n	field (INPA, %s)\n	field (CALC, %s)\n	field (FLNK, %s)\n}\n" %(record_calc_field, INPA_field, CALC_field, FNLK_field))
	
	INPA_field = '"$(P)$(R)status"'
	INPB_field = '"$(P)$(R)disconnect-counter.LA"'
	INPC_field = '"$(P)$(R)disconnect-counter"'
	CALC_field = '"(A=0&&B=1)?C+1:C"'
	calc_field = '"$(P)$(R)disconnect-counter"'
	arquivo_saida.write("record (calc, %s) {\n	field (INPA, %s)\n	field (INPB, %s)\n	field (INPC, %s)\n	field (CALC, %s)\n}\n" %(calc_field, INPA_field, INPB_field, INPC_field, CALC_field))

def escreve_record_ai(nome_da_variavel, PLC_name, offset, _type):
	INP_field = '"@%s/%d T=%s"' %(PLC_name, offset, _type)
	ai_field = '"$(P)$(R)%s"' %(nome_da_variavel)
	arquivo_saida.write("\nrecord (ai, %s) {\n	field (SCAN, %s)\n	field (DTYP, %s)\n	field (INP, %s)\n}\n" %(ai_field, SCAN_field, DTYP_field, INP_field))

def escreve_record_bi(nome_da_variavel, PLC_name, bit, offset, _type):
	INP_field = '"@%s/%d B=%d T=%s"' %(PLC_name, bit, offset, _type)
	bi_field = '"$(P)$(R)%s"' %(nome_da_variavel)
	arquivo_saida.write("\nrecord (bi, %s) {\n	field (SCAN, %s)\n	field (DTYP, %s)\n	field (INP, %s)\n}\n" %(bi_field, SCAN_field, DTYP_field, INP_field))

def escreve_record_bo(nome_da_variavel, PLC_name, bit, offset, _type):
	OUT_field = '"@%s/%d B=%d T=%s"' %(PLC_name, bit, offset, _type)
	bo_field = '"$(P)$(R)%s"' %(nome_da_variavel)
	PINI_field = '"YES"'
	arquivo_saida.write("\nrecord (bo, %s) {\n	field (DTYP, %s)\n	field (OUT, %s)\n	field (PINI, %s)\n}\n" %(bo_field, DTYP_field, OUT_field, PINI_field))	

def escreve_record_ao(nome_da_variavel, PLC_name, offset, _type):
	OUT_field = '"@%s/%d T=%s"' %(PLC_name, offset, _type)
	ao_field = '"$(P)$(R)%s"' %(nome_da_variavel)
	arquivo_saida.write("\nrecord (ao, %s) {\n	field (DTYP, %s)\n	field (OUT, %s)\n}\n" %(ao_field, DTYP_field, OUT_field))

escreve_cabecario(nome_comunicacao[0])

for line in arquivo_entrada:
        if numeroLinha == 0:
                vetorOffset = line.split(",")
	if numeroLinha == 1:
		vetorOffset_write = line.split(",")
        if line == "***\n":
		flag_transicao = 1

	if flag_transicao != 1 and numeroLinha != 0 and numeroLinha != 1:
		campos = line.split(",")
		print campos	# Debbug
		nome_da_variavel = campos[0]
		tipo_da_variavel_antiga = tipo_da_variavel_atual
		tipo_da_variavel = campos[2]
		tipo_da_variavel_atual = campos[2]
		cat_da_variavel_antiga = cat_da_variavel_atual
		cat_da_variavel_atual = campos[1]
		
		if cat_da_variavel_atual != cat_da_variavel_antiga and cat_da_variavel_antiga != "":
			#print "Houve transicao de categoria"	# Debugg
			if nome_da_variavel[len(nome_da_variavel)-2:] == '_W':
				numero_bits[1] = 0
				offset[1] =  int(vetorOffset_write[indiceVetorOffset[1]+1])
				#print (offset[porta])	# Debugg
				tamanho_total[1] = offset[1]
				indiceVetorOffset[1] += 1
			else:
				numero_bits[0] = 0
				offset[0] =  int(vetorOffset_write[indiceVetorOffset[0]+1])
				#print (offset[porta])	# Debugg
				tamanho_total[0] = offset[1]
				indiceVetorOffset[0] += 1				
	
		if tipo_da_variavel == "Word\n":
				if nome_da_variavel[len(nome_da_variavel)-2:] == '_W':
					escreve_record_ao(nome_da_variavel, nome_comunicacao[1], offset[1], "WORD")
					offset[1] += 2
					tamanho_total[1] +=2
				else:
					escreve_record_ai(nome_da_variavel, nome_comunicacao[0], offset[0], "WORD")
					offset[0] += 2
					tamanho_total[0] +=2					
 
		if tipo_da_variavel == "Real\n":
				if nome_da_variavel[len(nome_da_variavel)-2:] == '_W':			
					escreve_record_ao(nome_da_variavel, nome_comunicacao[1], offset[1], "REAL32")				
					offset[1] += 4
					tamanho_total[1] += 4
				else:
					escreve_record_ai(nome_da_variavel, nome_comunicacao[0], offset[0], "REAL32")				
					offset[0] += 4
					tamanho_total[0] += 4
					
		if tipo_da_variavel == "Int\n":
				if nome_da_variavel[len(nome_da_variavel)-2:] == '_W':
					escreve_record_ao(nome_da_variavel, nome_comunicacao[1], offset[1], "INT16")				
					offset[1] += 2
					tamanho_total[1] += 2					
				else:
					escreve_record_ai(nome_da_variavel, nome_comunicacao[0], offset[0], "INT16")				
					offset[0] += 2
					tamanho_total[0] += 2
				
		if tipo_da_variavel == "Bool\n":
				if nome_da_variavel[len(nome_da_variavel)-2:] == '_W':
					escreve_record_bo(nome_da_variavel, nome_comunicacao[1], offset[1], numero_bits[1], "BYTE")								
					numero_bits[1] = numero_bits[1] + 1				

					if numero_bits[1] == 8:
						offset[1] += 1
						tamanho_total[1] += 1
						numero_bits[1] = 0					
				else:
					escreve_record_bi(nome_da_variavel, nome_comunicacao[0], offset[0], numero_bits[0], "BYTE")								
					numero_bits[0] = numero_bits[0] + 1				

					if numero_bits[0] == 8:
						offset[0] += 1
						tamanho_total[0] += 1
						numero_bits[0] = 0	

		
	flag_transicao = 0
	numeroLinha += 1

print tamanho_total
arquivo_saida.close()
