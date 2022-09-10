package metamorphic.visitors;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;

import java.util.List;

public interface CuListGet {
    public List getList(CompilationUnit cu);
}
