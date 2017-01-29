#!/usr/bin/python
import sys

file_in = str(sys.argv[1])
file_out = str(sys.argv[2])
arquivo_entrada = open(file_in, 'r')
arquivo_saida = open(file_out, 'a')

nome_comunicacao = ("Testsystem1:0","Testesystem2:0")
SCAN_field = '"I/O Intr"'
DTYP_field = '"S7plc"'

flag_transicao = 0
offset = [0]*2
numero_bits = 0
tamanho_total = [0]*2
porta = 0
	
def escreve_cabecario(PLC_name):
	INP_field_cab = '"@%s"' %(PLC_name)	
	ZNAM_field = '"disconnected"'
	ONAM_field = '"connected"'
	ZSV_field = '"MAJOR"'
	DTYP_field_cab = '"S7plc stat"'
	FLNK_field = '"$(P)$(R)status-counter"'	
	arquivo_saida.write("record (bi, $(P)$(R)status) {\n	field (DTYP, %s)\n	field (INP, %s)\n	field (SCAN, %s)\n	field (ZNAM, %s)\n	field (ONAM, %s)\n	field (ZSV, %s)\n	field(FLNK, %s)\n}\n" %(DTYP_field_cab, INP_field_cab, SCAN_field, ZNAM_field, ONAM_field, ZSV_field, FLNK_field))
	
	CALC_field = '"A+1"'
	FNLK_field = '"$(P)$(R)disconnect-counter"'
	arquivo_saida.write("record (calc, $(P)$(R)status-counter) {\n	field (INPA, $(P)$(R)status-counter)\n	field (CALC, %s)\n	field (FLNK, %s)\n}\n" %(CALC_field, FNLK_field))
	
	INPB_field = '"$(P)$(R)disconnect-counter.LA"'
	INPC_field = '"$(P)$(R)disconnect-counter"'
	CALC_field = '"(A=0&&B=1)?C+1:C"'	
	arquivo_saida.write("record (calc, $(P)$(R)disconnect-counter) {\n	field (INPA, $(P)$(R)status)\n	field (INPB, %s)\n	field (INPC, %s)\n	field (CALC, %s)\n}\n" %(INPB_field, INPC_field, CALC_field))

def escreve_record_ai(nome_da_variavel, PLC_name, offset, _type):
	INP_field = '"@%s/%d T=%s"' %(PLC_name, offset, _type)
	arquivo_saida.write("\nrecord (ai, $(P)$(R)%s) {\n	field (SCAN, %s)\n	field (DTYP, %s)\n	field (INP, %s)\n}\n" %(nome_da_variavel, SCAN_field, DTYP_field, INP_field))

def escreve_record_bi(nome_da_variavel, PLC_name, bit, offset, _type):
	INP_field = '"@%s/%d B=%d T=%s"' %(PLC_name, bit, offset, _type)
	arquivo_saida.write("\nrecord (bi, $(P)$(R)%s) {\n	field (SCAN, %s)\n	field (DTYP, %s)\n	field (INP, %s)\n}\n" %(nome_da_variavel, SCAN_field, DTYP_field, INP_field))


escreve_cabecario(nome_comunicacao[0])

for line in arquivo_entrada:

        if line == "\n":
		flag_transicao = 1
		porta += 1 

	if flag_transicao != 1:
		campos = line.split(";")
		nome_da_variavel = campos[0]
		tipo_da_variavel = campos[1]
		
		if tipo_da_variavel == "Real\n":
				escreve_record_ai(nome_da_variavel, nome_comunicacao[porta], offset[porta], "REAL32")				
				offset[porta] += 4
				tamanho_total[porta] += 4
				
		if tipo_da_variavel == "Bool\n":
				escreve_record_bi(nome_da_variavel, nome_comunicacao[porta], offset[porta], numero_bits, "BYTE")								
				numero_bits = numero_bits + 1				
				if numero_bits == 8:
					offset[porta] += 1
					tamanho_total[porta] += 1
					numero_bits = 0	

		
	flag_transicao = 0

print tamanho_total
arquivo_saida.close()
