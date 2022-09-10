package metamorphic;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;

public abstract class Generator {
    public abstract GeneratedDate generate(MethodDeclaration md, String diffLine, String diffLineIndex);
    //public abstract String getBuggyLineIndex();
    @Override
    public abstract String toString();
    public GeneratedDate generate(CompilationUnit cu, MethodDeclaration md, String diffLine, String diffLineIndex){
        GeneratedDate generated = generate(md, diffLine, diffLineIndex);
        if(generated==null) return null;
        if(!generated.generateSuccess) return null;
        generated.java = cu.toString();
        if(generated.diffLineIndex==null) generated.diffLineIndex = diffLineIndex;
        if(generated.diffLine==null) generated.diffLine = diffLine;
        return generated;
    }



}

class GeneratedDate{
    boolean generateSuccess = false;
    String diffLine = null;
    String diffLineIndex = null;
    String change = null;
    String method = null;
    String java = null;
}