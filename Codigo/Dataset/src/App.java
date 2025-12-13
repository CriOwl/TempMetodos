import java.io.File;
import java.io.FileWriter;
import java.util.Scanner;

public class App {
    
    public static void main(String[] args) throws Exception {
        try {
            File file= new File("/home/criowl/Criowl/RigelSirius/train-metadata.csv");
            FileWriter writer = new FileWriter("/home/criowl/Criowl/RigelSirius/processed_data.csv");
            Scanner scanner = new Scanner(file);
            String line = scanner.nextLine();
                String[] values = line.split(",");
                writer.write(values[1]+","+values[6]+","+values[19]+","+values[20]+","+values[21]+","+values[26]+","+values[30]+","+values[32]+","+values[38]+","+values[39]+"\n");

            while (scanner.hasNextLine()) { 
                String line2 = scanner.nextLine();
                String[] values2= line2.split(",");
                if (values2[8].contains("3D: XP")) {
                    writer.write(values2[1]+","+values2[6]+","+","+values2[19]+","+values2[20]+","+values2[21]+","+values2[26]+","+values2[30]+","+values2[32]+","+values2[38]+","+values2[39]+"\n");
                } 
            } 
            
            writer.close();
        } catch (Exception e) {
            System.out.println(e);
        }
        // 1 
        /*
        "target"----1
        "clin_size_long_diam_mm"----6
        "tbp_tile_type"----8
        "tbp_lv_areaMM2"----19
        "tbp_lv_area_perim_ratio"----20
        "tbp_lv_color_std_mean"----21
        "tbp_lv_deltaLBnorm"----26
        "tbp_lv_minorAxisMM"----30
        "tbp_lv_norm_border"----32
        "tbp_lv_symm_2axis"----38
        "tbp_lv_symm_2axis_angle"----39
        */
        
        
    }
}
