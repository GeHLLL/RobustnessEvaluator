package metamorphic.visitors;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.AnnotationDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.ArrayList;
import java.util.List;

public class NameExprVisitor extends VoidVisitorAdapter<List<NameExpr>>{
    @Override
    public void visit(NameExpr n, List<NameExpr> list) {
        super.visit(n, list);
        list.add(n);
    }



    public static List<NameExpr> getList(MethodDeclaration md) {
        List<NameExpr> list = new ArrayList<>();
        NameExprVisitor visitor = new NameExprVisitor();
        visitor.visit(md, list);
        return list;
    }


    public static List<NameExpr> getList(CompilationUnit cu) {
        List<NameExpr> list = new ArrayList<>();
        NameExprVisitor visitor = new NameExprVisitor();
        visitor.visit(cu, list);
        return list;
    }

    public static List<NameExpr> getList(Expression expression) {
        List<NameExpr> list = new ArrayList<>();
        NameExprVisitor visitor = new NameExprVisitor();
        if(expression instanceof MethodCallExpr) visitor.visit((MethodCallExpr) expression, list);
        if(expression instanceof FieldAccessExpr) visitor.visit((FieldAccessExpr) expression, list);
        if(expression instanceof NameExpr) visitor.visit((NameExpr) expression, list);
        return list;
    }


}
