import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class MainProcessaCotacoesBolsa {

	public static void main(String[] args) throws IOException {
		if (args.length >= 1) {
			BufferedReader reader = null;
			BufferedWriter writer = null;
			try {
				String processedFile = args[0].toUpperCase().replace(".TXT", "_PROCESSED" + (args.length >= 2 ? "_" + args[1].toUpperCase() + ".CSV" : ".CSV"));
				if (processedFile.equals(args[0])) {
					throw new RuntimeException("Nome de arquivo [" + args[0] + "] é inválido: deve ter extensão");
				}
				
				reader = new BufferedReader(new FileReader(new File(args[0])));
				writer = new BufferedWriter(new FileWriter(new File(processedFile)));
				writer.write("Reg;Data;BDI;Ticker;TpMerc;Empresa;Espec;PrazoT;Moeda;Abertura;Máximo;Mínimo;Médio;Fechamento;Melhor Compra;Melhor Venda;Qtde Neg;Qtde Tit;Volume;PreExe;IndOPC;Vcto;Fator Cot;PtoExe;CodISIN;DisMes");
				String line = null;
				
				System.out.println("Processando arquivo...");
				
				int cont = 0;
				while (reader.ready()) {
					line = reader.readLine();
					//Only stock history
					if (line.startsWith("01")) {
						cont++;
						if (cont % 10000 == 0) 
							System.out.println(cont + " linhas já foram processadas.");
						
						//Filters by stock code
						if (args.length == 1
						 || args.length >= 2 && args[1].equals(line.substring(12, 24).trim())) {
							writer.write("\n" + line.substring(0, 2) 
								+ ";" + line.substring(2, 10)
								+ ";" + line.substring(10, 12)
								+ ";" + line.substring(12, 24)
								+ ";" + line.substring(24, 27)
								+ ";" + line.substring(27, 39)
								+ ";" + line.substring(39, 49)
								+ ";" + line.substring(49, 52)
								+ ";" + line.substring(52, 56)
								+ ";" + line.substring(56, 69)
								+ ";" + line.substring(69, 82)
								+ ";" + line.substring(82, 95)
								+ ";" + line.substring(95, 108)
								+ ";" + line.substring(108, 121)
								+ ";" + line.substring(121, 134)
								+ ";" + line.substring(134, 147)
								+ ";" + line.substring(147, 152)
								+ ";" + line.substring(152, 170)
								+ ";" + line.substring(170, 188)
								+ ";" + line.substring(188, 201)
								+ ";" + line.substring(201, 202)
								+ ";" + line.substring(202, 210)
								+ ";" + line.substring(210, 217)
								+ ";" + line.substring(217, 230)
								+ ";" + line.substring(230, 242)
								+ ";" + line.substring(242, 245));
						}
					}
				}
				System.out.println("Terminado! Arquivo gerado: " + processedFile);
			} catch (Exception e) {
				System.err.println("Erro: " + e.getMessage());
			} finally {
				if (reader != null) reader.close();
				if (writer != null) writer.close();
			}
		} else {
			System.err.println("É necessário passar o nome do arquivo como parâmetro.");
		}
	}

}
