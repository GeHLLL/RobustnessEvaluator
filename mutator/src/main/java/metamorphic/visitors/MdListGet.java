package metamorphic.visitors;


import com.github.javaparser.ast.body.MethodDeclaration;

import java.util.List;

public interface MdListGet {
    public List getList(MethodDeclaration md);
}
