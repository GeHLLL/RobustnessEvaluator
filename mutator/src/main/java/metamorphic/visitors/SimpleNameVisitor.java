package metamorphic.visitors;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.AnnotationDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.ArrayList;
import java.util.List;

public class SimpleNameVisitor extends VoidVisitorAdapter<List<SimpleName>>{
    @Override
    public void visit(SimpleName n, List<SimpleName> list) {
        super.visit(n, list);
        list.add(n);
    }


    public static List<SimpleName> getList(CompilationUnit cu) {
        List<SimpleName> list = new ArrayList<>();
        SimpleNameVisitor visitor = new SimpleNameVisitor();
        visitor.visit(cu, list);
        return list;
    }

    public static List<SimpleName> getList(MethodDeclaration md) {
        List<SimpleName> list = new ArrayList<>();
        SimpleNameVisitor visitor = new SimpleNameVisitor();
        visitor.visit(md, list);
        return list;
    }
}
