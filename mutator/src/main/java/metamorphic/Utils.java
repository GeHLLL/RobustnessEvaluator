package metamorphic;

import com.github.javaparser.ast.CompilationUnit;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;

public class Utils {
    static String getTxtPath(String dirPath, String index){ return dirPath + "\\" + index + ".txt"; }
    static String pathJoin(String path, String name){ return path + "\\" + name; }
    static void myWrite(String path, String index, String str) throws IOException {
        path = getTxtPath(path, index);
        Files.write(Paths.get(path), str.getBytes("utf-8"));
    }
    static String readFile(String path) throws IOException {
        return new String(Files.readAllBytes(Paths.get(path)));
    }

}
