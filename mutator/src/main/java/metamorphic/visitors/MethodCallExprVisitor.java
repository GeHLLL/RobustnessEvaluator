package metamorphic.visitors;

import com.github.javaparser.ast.body.AnnotationDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.ArrayList;
import java.util.List;

public class MethodCallExprVisitor extends VoidVisitorAdapter<List<MethodCallExpr>> {
    @Override
    public void visit(MethodCallExpr n, List<MethodCallExpr> list) {
        super.visit(n, list);
        list.add(n);
    }

    public static List<MethodCallExpr> getList(MethodDeclaration method){
        List<MethodCallExpr> list = new ArrayList<>();
        MethodCallExprVisitor methodCallExprVisitor = new MethodCallExprVisitor();
        methodCallExprVisitor.visit(method, list);
        return list;
    }
}
