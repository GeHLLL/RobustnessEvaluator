package metamorphic.visitors;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.ArrayList;
import java.util.List;

public class MethodDeclarationVisitor extends VoidVisitorAdapter<List<MethodDeclaration>> implements CuListGet {
    @Override
    public void visit(MethodDeclaration n, List<MethodDeclaration> list) {
        super.visit(n, list);
        list.add(n);
    }

    @Override
    public List<MethodDeclaration> getList(CompilationUnit cu) {
        List<MethodDeclaration> list = new ArrayList<>();
        MethodDeclarationVisitor visitor = new MethodDeclarationVisitor();
        visitor.visit(cu, list);
        return list;
    }
}
