package metamorphic.visitors;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;

import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import metamorphic.Variable;

import java.util.ArrayList;
import java.util.List;

public class VariableDeclaratorVisitor extends VoidVisitorAdapter<List<Variable>> implements CuListGet, MdListGet{
    @Override
    public void visit(VariableDeclarator n, List<Variable> list) {
        super.visit(n, list);
        list.add(new Variable(n));
    }

    @Override
    public List<Variable> getList(CompilationUnit cu) {
        List<Variable> list = new ArrayList<>();
        VariableDeclaratorVisitor visitor = new VariableDeclaratorVisitor();
        visitor.visit(cu, list);
        return list;
    }

    public List<Variable> getList(MethodDeclaration md) {
        List<Variable> list = new ArrayList<>();
        VariableDeclaratorVisitor visitor = new VariableDeclaratorVisitor();
        visitor.visit(md, list);
        return list;
    }


}
