package metamorphic.visitors;

import com.github.javaparser.ast.body.AnnotationDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.ArrayList;
import java.util.List;

public class AssignExprVisitor extends VoidVisitorAdapter<List<AssignExpr>> {
    @Override
    public void visit(AssignExpr n, List<AssignExpr> list) {
        super.visit(n, list);
        list.add(n);
    }

    public static List<AssignExpr> getList(MethodDeclaration method){
        List<AssignExpr> list = new ArrayList<>();
        AssignExprVisitor assignExprVisitor = new AssignExprVisitor();
        assignExprVisitor.visit(method, list);
        return list;
    }
}
