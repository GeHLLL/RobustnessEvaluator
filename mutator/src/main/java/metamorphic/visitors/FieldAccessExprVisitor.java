package metamorphic.visitors;

import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import metamorphic.Variable;

import java.util.ArrayList;
import java.util.List;

public class FieldAccessExprVisitor extends VoidVisitorAdapter<List<FieldAccessExpr>> implements MdListGet{
    @Override
    public void visit(FieldAccessExpr n, List<FieldAccessExpr> list) {
        super.visit(n, list);
        list.add(n);
    }


    @Override
    public List<FieldAccessExpr> getList(MethodDeclaration md) {
        List<FieldAccessExpr> list = new ArrayList<>();
        FieldAccessExprVisitor visitor = new FieldAccessExprVisitor();
        visitor.visit(md, list);
        return list;
    }
}
