package metamorphic.visitors;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import metamorphic.Variable;

import java.util.ArrayList;
import java.util.List;

public class ParameterVisitor extends VoidVisitorAdapter<List<Variable>> implements CuListGet, MdListGet{
    @Override
    public void visit(Parameter n, List<Variable> list) {
        super.visit(n, list);
        list.add(new Variable(n));
    }



    @Override
    public List<Variable> getList(CompilationUnit cu) {
        List<Variable> list = new ArrayList<>();
        ParameterVisitor visitor = new ParameterVisitor();
        visitor.visit(cu, list);
        return list;

    }

    public List<Variable> getList(MethodDeclaration md) {
        List<Variable> list = new ArrayList<>();
        ParameterVisitor visitor = new ParameterVisitor();
        visitor.visit(md, list);
        return list;
    }
}
