import java.io.*;
import java.nio.file.*;

public class App {

    public static void main(String[] args) {
        Path input = Paths.get("Codigo/Dataset/src/train-metadata.csv");
        Path output = Paths.get("processed_data.csv");
        System.out.println(output.toAbsolutePath().toString());
        try (
            BufferedReader br = Files.newBufferedReader(input);
            BufferedWriter bw = Files.newBufferedWriter(output)
        ) {

            String line = br.readLine();
            String[] values = line.split(",");

            bw.write(values[1] + "," + values[6] + "," + values[19] + "," +
                     values[34] + "," + values[21] + "," + values[26] + "," +
                     values[30] + "," + values[32] + "," + values[38] + "," +
                     values[39]);
            bw.newLine();

            int i = 0;
            while ((line = br.readLine()) != null) {
                i++;

                // Mostrar progreso cada 100k líneas
                if (i % 100_000 == 0) {
                    System.out.println("Procesadas: " + i);
                }

                String[] v = line.split(",");

                if (v.length > 39 && v[8].contains("3D: XP")) {
                    bw.write(
                        v[1] + "," + v[6] + "," +
                        v[19] + "," + v[34] + "," + v[21] + "," +
                        v[26] + "," + v[30] + "," + v[32] + "," +
                        v[38] + "," + v[39]
                    );
                    bw.newLine();
                }
            }

            System.out.println("Proceso finalizado. Total líneas: " + i);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}