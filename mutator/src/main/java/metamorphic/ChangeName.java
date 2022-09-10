package metamorphic;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.CastExpr;
import com.github.javaparser.ast.expr.EnclosedExpr;
import com.github.javaparser.ast.expr.SimpleName;
import metamorphic.visitors.*;


import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ChangeName extends Generator{

    //使用该方法时无需再variableNames中去除被改变名字者，因为和原名重名也是不被允许的
    private String getNewName(String type, List<String> variableNames){

        NameAnalysis nameAnalysis = new NameAnalysis();
        List<String> names = nameAnalysis.getNameList(type);
        Collections.shuffle(names);
        while(names.size()>0){
            String newName = names.get(0);
            names.remove(newName);
            if(!variableNames.contains(newName)) return newName;
        }
        return "";
    }

    private boolean isBaseType(String type){
        String[] baseTypeArray = {"byte", "short", "int", "long", "float", "double", "char", "boolean", "Boolean", "Long", "Short", "Double", "Float", "Byte"};
        for(String baseType: baseTypeArray){
            if(type.equals(baseType)) return true;
        }
        return false;
    }

    public boolean isInBlackList(String name){
        String[] blackList = {"args"};
        for(String blackName: blackList){
            if(blackName.equals(name)) return true;
        }
        return false;
    }

    public Variable chooseVariable(List<Variable> variableList){
        Collections.shuffle(variableList);
        while(variableList.size()>0){
            Variable choosed = variableList.get(0);
            variableList.remove(choosed);
            if(!(isBaseType(choosed.getTypeAsString()) || isInBlackList(choosed.getNameAsString()))) return choosed;

        }
        return null;
    }

    //获得两个字符串 第一个是oldname-》newname 第二个是代码
    @Override
    public GeneratedDate generate(MethodDeclaration md, String buggyLine, String buggyLineIndex){
        //String[] res = new String[2];
        GeneratedDate generatedDate = new GeneratedDate();
        VariableDeclaratorVisitor vdVisitor = new VariableDeclaratorVisitor();
        ParameterVisitor paraVisitor = new ParameterVisitor();
        List<Variable> variableList = new ArrayList<>();
        variableList.addAll(vdVisitor.getList(md));
        variableList.addAll(paraVisitor.getList(md));

        List<String> variableNameList = new ArrayList<>();
        for(Variable variable: variableList){
            variableNameList.add(variable.getNameAsString());
        }

        Variable changedNode = chooseVariable(variableList);

        if(changedNode==null) return null;

        String changedName = changedNode.getNameAsString();
        String type = changedNode.getTypeAsString();

        String newName = getNewName(type, variableNameList);

        if(newName.equals("")) return null;

        List<SimpleName> simpleNameList = SimpleNameVisitor.getList(md);
        for(SimpleName simpleName: simpleNameList){
            if(simpleName.getIdentifier().equals(changedName)){
                simpleName.setIdentifier(newName);
            }
        }



        String[] methodLines = md.toString().split("\n");
        buggyLine = methodLines[Integer.parseInt(buggyLineIndex)];
        generatedDate.diffLine = buggyLine;
        generatedDate.change = changedName + "->" + newName;
        generatedDate.method = md.toString();
        generatedDate.generateSuccess = true;
        return generatedDate;
    }

    @Override
    public String toString() {
        return "ChangeName";
    }
    //获得两个字符串 第一个是oldname-》newname 第二个是代码
    /*public String[] generate(CompilationUnit cu, MethodDeclaration md){
        String[] res = new String[2];

        VariableDeclaratorVisitor vdVisitor = new VariableDeclaratorVisitor();
        ParameterVisitor paraVisitor = new ParameterVisitor();
        List<Variable> variableList = new ArrayList<>();
        variableList.addAll(vdVisitor.getList(cu));
        variableList.addAll(paraVisitor.getList(cu));

        List<String> variableNameList = new ArrayList<>();
        for(Variable variable: variableList){
            variableNameList.add(variable.getNameAsString());
        }

        Variable changedNode = chooseVariable(variableList);

        if(changedNode==null) return null;

        String changedName = changedNode.getNameAsString();
        String type = changedNode.getTypeAsString();

        String newName = getNewName(type, variableNameList);

        if(newName.equals("")) return null;

        List<SimpleName> simpleNameList = SimpleNameVisitor.getList(cu);
        for(SimpleName simpleName: simpleNameList){
            if(simpleName.getIdentifier().equals(changedName)){
                simpleName.setIdentifier(newName);
            }
        }
        //System.out.println(changedName + "->" + newName);

        res[0] = changedName + "->" + newName;
        res[1] = cu.toString();

        return res;
    }*/

    public static void main(String[] args) throws FileNotFoundException {
        ChangeName changeName = new ChangeName();
        String path = "F:\\workspace\\bug_detection\\mutation\\src\\main\\java\\metamorphic\\Demo.java";
        /*CompilationUnit cu = StaticJavaParser.parse(new File(path));
        MethodDeclarationVisitor methodDeclarationVisitor = new MethodDeclarationVisitor();
        List<MethodDeclaration> methodDeclarationList = methodDeclarationVisitor.getList(cu);
        String[] res = changeName.changeMethod(methodDeclarationList.get(0));
        System.out.println(res[0]);
        System.out.println(res[1]);*/

        //changeName.changeName(cu);
       /* String[] res = changeName.generate(cu);
        System.out.println(res[0]);
        System.out.println(res[1]);*/
        //EnclosedExpr enclosedExpr = new EnclosedExpr();
        //CastExpr
    }


}
