arquivo_saida = open("saida.txt",'a')

SCAN_field = '"I/O Intr"'
DTYP_field = '"S7plc"'



def escreve_record_ai(nome_da_variavel, PLC_name, offset, _type):
	INP_field = '"@%s/%d T=%s"' %(PLC_name, offset, _type)
	arquivo_saida.write("\nrecord (ai, $(P)$(R)%s) {\n	field (SCAN, %s)\n	field (DTYP, %s))\n	field (INP, %s)\n}\n" %(nome_da_variavel, SCAN_field, DTYP_field, INP_field))

escreve_record_ai("valvula1", "Systemsend:0", 2, "Real32")

def escreve_record_bi(nome_da_variavel, PLC_name, offset, _type):
	INP_field = '"@%s/%d T=%s"' %(PLC_name, offset, _type)
	arquivo_saida.write("\nrecord (bi, $(P)$(R)%s) {\n	field (SCAN, %s)\n	field (DTYP, %s))\n	field (INP, %s)\n}\n" %(nome_da_variavel, SCAN_field, DTYP_field, INP_field))

escreve_record_bi("valvula2", "Systemsend:0", 2, "BYTE")
