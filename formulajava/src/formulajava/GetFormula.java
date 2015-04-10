package formulajava;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;

import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;

public class GetFormula {

	public void getFormula(String filepath, String outpath) throws IOException{
		String restr = "";
		
		FileInputStream fis = new FileInputStream(filepath);
		Workbook wb = new HSSFWorkbook(fis); //or new XSSFWorkbook("c:/temp/test.xls")
		for (int sheetnum = 0; sheetnum < wb.getNumberOfSheets(); sheetnum++){
			Sheet sheet = wb.getSheetAt(sheetnum);
			String sheetname = wb.getSheetName(sheetnum);
		
			for (Row row : sheet){
				for(Cell cell : row) {
				     if(cell.getCellType() == Cell.CELL_TYPE_FORMULA) {
				    	 restr += filepath+"||"+sheetname + "||"+ cell.getRowIndex()+"||"+cell.getColumnIndex()+"||"+cell.getCellFormula()+"\n";
//				    	System.out.println(filepath+"||"+cell.getRowIndex()+"||"+cell.getColumnIndex()+"||"+cell.getCellFormula());
//				        switch(cell.getCachedFormulaResultType()) {
//				            case Cell.CELL_TYPE_NUMERIC:
//				                System.out.println("Last evaluated as: " + cell.getNumericCellValue());
//				                break;
//				            case Cell.CELL_TYPE_STRING:
//				                System.out.println("Last evaluated as \"" + cell.getRichStringCellValue() + "\"");
//				                break;
//				        }
				     }
				 }
			}
		}
		
		try{
			FileWriter fw = new FileWriter(new File(outpath));
			BufferedWriter bw = new BufferedWriter(fw);
			
			bw.write(restr);
			
			bw.close();
			fw.close();
		}catch(Exception e){
			e.printStackTrace();
		}

	}
	
	
	public static void main(String[] args) throws Exception{
		
		if(args.length != 2){
			System.out.println("Jar: Get spreadsheets formulas in dir");
			System.out.println("Input: inputpath, outpath");
			return;
		}
////		String filepath = "/home/cz/test";
		String inputpath = args[0];
		String outpath = args[1];
		
//		String dirpath = "/z/chenzhe-data/spreadsheet/webexcel/webexcel_sample5000";
//		String outpath = "/z/chenzhe-data/spreadsheet/webexcel/formulainfo.txt";
//		
		
		
		GetFormula getformula = new GetFormula();
//		getformula.getFormulaFromDir(dirpath, outpath);
		getformula.getFormula(inputpath, outpath);
		
	}
	
}
