package metamorphic;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.type.Type;
import metamorphic.visitors.*;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Random;

public class AddCast extends Generator{
    private Random random = new Random();

    private List<Variable> getVariables(MethodDeclaration method){
        VariableDeclaratorVisitor vdVisitor = new VariableDeclaratorVisitor();
        ParameterVisitor paraVisitor = new ParameterVisitor();
        List<Variable> variableList = new ArrayList<>();
        variableList.addAll(vdVisitor.getList(method));
        variableList.addAll(paraVisitor.getList(method));

        return variableList;
    }

    public List<NameExpr> getCastableName(MethodDeclaration method) {
        List<NameExpr> res = new ArrayList<>();


        //VariableDeclarator部分
        VariableDeclaratorVisitor vdVisitor = new VariableDeclaratorVisitor();
        List<Variable> variables = vdVisitor.getList(method);
        List<VariableDeclarator> variableDeclaratorList = new ArrayList<>();
        for(Variable variable: variables) variableDeclaratorList.add((VariableDeclarator) variable.getNode());

        for(VariableDeclarator variableDeclarator: variableDeclaratorList){
            Expression expression;
            Optional<Expression> expressionOptional = variableDeclarator.getInitializer();
            if(expressionOptional.isPresent()){
                expression = expressionOptional.get();
            }else {
                continue;
            }
            List<NameExpr> nameExprList = NameExprVisitor.getList(expression);
            res.addAll(nameExprList);
        }

        //AssignExpr部分
        List<AssignExpr> assignExprList = AssignExprVisitor.getList(method);
        for(AssignExpr assignExpr: assignExprList){
            Expression expression = assignExpr.getValue();
            List<NameExpr> nameExprList = NameExprVisitor.getList(expression);
            res.addAll(nameExprList);
        }

        //纯粹MethodCall部分
        List<MethodCallExpr> methodCallExprList = MethodCallExprVisitor.getList(method);
        for(MethodCallExpr methodCallExpr: methodCallExprList){
            List<NameExpr> nameExprList = NameExprVisitor.getList(methodCallExpr);
            for(NameExpr nameExpr: nameExprList){
                if(!res.contains(nameExpr)) res.add(nameExpr);
            }
        }

        return res;

    }
    public GeneratedDate generate(MethodDeclaration md, String buggyLine, String buggyLineIndex){
        //String[] res = new String[2];
        GeneratedDate generatedDate = new GeneratedDate();
        StringBuilder change = new StringBuilder();
        //List<SimpleName> simpleNameList = SimpleNameVisitor.getList(method);
        List<NameExpr> castableNameExprList = getCastableName(md);

        List<Variable> variableList = getVariables(md);

        /*for(Variable variable: variableList){
            SimpleName variableName = variable.getName();
            if(simpleNameList.contains(variableName)) simpleNameList.remove(variableName);

        }*/

        /*FieldAccessExprVisitor fieldAccessExprVisitor = new FieldAccessExprVisitor();
        List<FieldAccessExpr> fieldAccessExprList = fieldAccessExprVisitor.getList(method);
        //getName获取到的就是属性本身,getScope获取到的是对象
        for(FieldAccessExpr fieldAccessExpr: fieldAccessExprList){
            SimpleName fieldAccessName = fieldAccessExpr.getName();
            if(simpleNameList.contains(fieldAccessName)) simpleNameList.remove(fieldAccessName);
        }*/

        Variable choosedVariable = null;
        List<NameExpr> optionalNames = new ArrayList<>();
        //List<SimpleName> optionalNames = new ArrayList<>();
        while(optionalNames.size()==0 && variableList.size()>0){
            choosedVariable = variableList.get(random.nextInt(variableList.size()));
            variableList.remove(choosedVariable);
            String variableName = choosedVariable.getName().getIdentifier();
            /*for(SimpleName simpleName: simpleNameList){
                if(simpleName.getIdentifier().equals(variableName)) optionalNames.add(simpleName);
            }*/
            for(NameExpr nameExpr: castableNameExprList){
                if(nameExpr.getName().getIdentifier().equals(variableName)) optionalNames.add(nameExpr);
            }
        }
        if (variableList.size()==0 && optionalNames.size()==0) return null;

        NameExpr choosedNameExpr = optionalNames.get(random.nextInt(optionalNames.size()));

        if(choosedVariable.getTypeAsString() == null || choosedVariable.getTypeAsString().length()==0){
            System.out.println(choosedVariable.getNameAsString());
            System.out.println(choosedVariable.getTypeAsString());
            return null;
        }
        change.append(choosedVariable.getNameAsString());
        ClassOrInterfaceType classOrInterfaceType = new ClassOrInterfaceType(choosedVariable.getTypeAsString());



        NameExpr newNameExpr = new NameExpr(new SimpleName(choosedNameExpr.getName().getIdentifier()));
        CastExpr castExpr = new CastExpr(classOrInterfaceType, newNameExpr);
        EnclosedExpr enclosedExpr = new EnclosedExpr(castExpr);

        /*Optional<Node> optionalParentNode = choosedNameExpr.getParentNode();
        if(!optionalParentNode.isPresent()) return null;
        Node parentNode = optionalParentNode.get();
        parentNode.replace(choosedNameExpr, enclosedExpr);*/
        choosedNameExpr.replace(enclosedExpr);
        change.append("->");
        change.append(enclosedExpr.toString());

        String[] methodLines = md.toString().split("\n");
        buggyLine = methodLines[Integer.parseInt(buggyLineIndex)];

        generatedDate.diffLine = buggyLine;
        generatedDate.generateSuccess = true;
        generatedDate.change = change.toString();
        generatedDate.method = md.toString();
        return generatedDate;
    }

    @Override
    public String toString() {
        return "AddCast";
    }

    /*@Override
    public String[] generate(CompilationUnit cu, MethodDeclaration md){
        String[] res = new String[2];

        MethodDeclarationVisitor methodDeclarationVisitor = new MethodDeclarationVisitor();
        List<MethodDeclaration> mdList = methodDeclarationVisitor.getList(cu);
        MethodDeclaration choosedMethod = mdList.get(random.nextInt(mdList.size()));

        String change = changeMethod(choosedMethod);
        if(change == null) return null;
        res[0] = change;
        res[1] = cu.toString();
        return res;
    }*/



    public static void main(String[] args) throws FileNotFoundException {
        String path = "F:\\workspace\\bug_detection\\mutation\\src\\main\\java\\metamorphic\\Demo.java";
        /*SimpleName sn = new SimpleName("a");
        NameExpr nameExpr = new NameExpr(sn);*/
        CompilationUnit cu = StaticJavaParser.parse(new File(path));
        AddCast addCast = new AddCast();
        /*String[] res = addCast.generate(cu);
        System.out.println(res[0]);
        System.out.println(res[1]);*/
        /*VariableDeclaratorVisitor visitor = new VariableDeclaratorVisitor();
        List<Variable> list = visitor.getList(cu);
        CastExpr castExpr = new CastExpr(list.get(0).getType(), nameExpr);
        EnclosedExpr enclosedExpr = new EnclosedExpr(castExpr);
        System.out.println(enclosedExpr.toString());
        NameExprVisitor nameExprVisitor = new NameExprVisitor();
        List<NameExpr> neList = nameExprVisitor.getList(cu);
        List<SimpleName> snList = SimpleNameVisitor.getList(cu);
        list.get(0).getNode().replace(list.get(0).getNode().getChildNodes().get(0),enclosedExpr);*/

    }
}
