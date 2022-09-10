package metamorphic;

import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.Parameter;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.type.Type;


public class Variable {
    private final Node node;
    public Variable(Node node){
        this.node = node;
    }
    public Node getNode(){
        return node;
    }

    public String getNameAsString(){
        if(node instanceof VariableDeclarator) return ((VariableDeclarator) node).getNameAsString();
        if(node instanceof Parameter) return ((Parameter) node).getNameAsString();
        else return null;
    }

    public String getTypeAsString(){
        if(node instanceof VariableDeclarator) return ((VariableDeclarator) node).getTypeAsString();
        if(node instanceof Parameter) return ((Parameter) node).getTypeAsString();
        else return null;
    }

    public Type getType(){
        if(node instanceof VariableDeclarator) return ((VariableDeclarator) node).getType();
        if(node instanceof Parameter) return ((Parameter) node).getType();
        return null;
    }

    public SimpleName getName(){
        if(node instanceof VariableDeclarator) return ((VariableDeclarator) node).getName();
        if(node instanceof Parameter) return ((Parameter) node).getName();
        return null;
    }
}
