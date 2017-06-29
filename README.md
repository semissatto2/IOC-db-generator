# IOC-db-generator
___
	Código para geração automática de arquivo de configuração de variáveis EPICS para s7plc. 
	O código também imprime (no terminal) o tamanho total do DataBlock
___
	Padrão de arquivo.csv:
	OffsetStructLeitura1, OffsetStructLeitura2, OffsetStructLeitura3,
	OffsetStructEscrita1, OffsetStructEscrita2, OffsetStructEscrita3,
	nomePV,categoriaPV,tipoVariavel
	
	OBS.:
	Os offsets são adquiridos a partir do DataBlock do TIA Portal
	Variáveis de escritas devem ter sufixo _W em seu nome
	É aconselhável deixar as variáveis do tipo Booleana no fim do DataBlock
	Acessar csv_files/ para referências
___	
	Execução:
	$ db-generator.py <arquivoEntrada.csv> <arquivoSaida.db>
	

	
	
	Guilherme Teixeira Semissatto - LNLS - 07/02/2017 - guilherme.semissatto@lnls.br
___
