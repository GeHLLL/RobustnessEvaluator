package metamorphic;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.expr.VariableDeclarationExpr;
import com.github.javaparser.ast.stmt.ExpressionStmt;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.type.Type;
import metamorphic.visitors.NameExprVisitor;
import metamorphic.visitors.ParameterVisitor;
import metamorphic.visitors.SimpleNameVisitor;
import metamorphic.visitors.VariableDeclaratorVisitor;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class NewVariable extends Generator{

    private List<Integer> getVDStatementPosList(List<Statement> statements){
        List<Integer> variableDeclarationExprPosList = new ArrayList<>();
        for(int i=0;i<statements.size();i++){
            if(statements.get(i).isExpressionStmt()){
                ExpressionStmt expressionStmt = statements.get(i).asExpressionStmt();
                if(expressionStmt.getExpression().isVariableDeclarationExpr()){
                    variableDeclarationExprPosList.add(i);
                }
            }
        }
        return variableDeclarationExprPosList;
    }

    private int getDiffLineIndex(MethodDeclaration md, String diffLine){
        diffLine = diffLine.trim();
        String method = md.toString();
        String[] lines = method.split("\n");
        for(int i=0;i<lines.length;i++){
            if(diffLine.equals(lines[i].trim())) return i;
        }
        return -1;
    }
    private int getNewDiffLineIndex(int diffLineIndex, Statement changedStatement){
        int changedLineIndex = changedStatement.getRange().get().begin.line;
        if(changedLineIndex < diffLineIndex) return diffLineIndex + 1;
        else return diffLineIndex;
    }

    private boolean isInBlackList(String name){
        String[] blackList = {"args"};
        for(String blackName: blackList){
            if(blackName.equals(name)) return true;
        }
        return false;
    }

    private boolean isBaseType(String type){
        String[] baseTypeArray = {"byte", "short", "int", "long", "float", "double", "char", "boolean", "Boolean", "Long", "Short", "Double", "Float", "Byte"};
        for(String baseType: baseTypeArray){
            if(type.equals(baseType)) return true;
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
    private String getNewName(VariableDeclarator vd, MethodDeclaration md){
        VariableDeclaratorVisitor vdVisitor = new VariableDeclaratorVisitor();
        ParameterVisitor paraVisitor = new ParameterVisitor();
        List<Variable> variableList = new ArrayList<>();
        variableList.addAll(vdVisitor.getList(md));
        variableList.addAll(paraVisitor.getList(md));

        List<String> variableNameList = new ArrayList<>();
        for(Variable variable: variableList){
            variableNameList.add(variable.getNameAsString());
        }

        List<String> names = new ArrayList<>();
        if(!(isBaseType(vd.getTypeAsString()) || isInBlackList(vd.getNameAsString()))){
            names.addAll(new NameAnalysis().getNameList(vd.getTypeAsString()));
        }
        names.add("var0");

        Collections.shuffle(names);
        while(names.size()>0){
            String newName = names.get(0);
            names.remove(newName);
            if(!variableNameList.contains(newName)) return newName;
        }

        return "";
    }
    private String getNewDiffLine(MethodDeclaration md, int diffLineIndex){
        String[] lines = md.toString().split("\n");
        return lines[diffLineIndex];
    }

    @Override
    public GeneratedDate generate(MethodDeclaration md, String diffLine, String buggyLineIndex) {
        GeneratedDate generatedDate = new GeneratedDate();

        int diffLineIndex = getDiffLineIndex(md, diffLine);
        if(diffLineIndex==-1) return null;

        List<Statement> statements = md.getBody().get().getStatements();
        List<Integer> vdStatementsPosList = getVDStatementPosList(statements);
        if(vdStatementsPosList.size()==0) return null;

        int changedVariablePos = vdStatementsPosList.get(new Random().nextInt(vdStatementsPosList.size()));
        Statement changedStatement = statements.get(changedVariablePos);



        VariableDeclarator changedVD = changedStatement.asExpressionStmt().getExpression().asVariableDeclarationExpr().getVariable(0);
        String variableName = changedVD.getNameAsString();
        //String variableType = changedVD.getTypeAsString();
        Type variableType = changedVD.getType();

        String newName = getNewName(changedVD, md);
        if(newName.equals("")) return null;

        //先把所有的变量名改掉，因为如果后面再改，会把赋值语句也改掉
        List<NameExpr> nameExprList = NameExprVisitor.getList(md);
        for(NameExpr nameExpr: nameExprList){
            if(nameExpr.getName().getIdentifier().equals(variableName)){
                nameExpr.getName().setIdentifier(newName);
            }
        }

        VariableDeclarator newVariableDeclarator = new VariableDeclarator(variableType.clone(), newName, new NameExpr(variableName));
        ExpressionStmt newExpressionStmt = new ExpressionStmt(new VariableDeclarationExpr(newVariableDeclarator));
        md.getBody().get().addStatement(changedVariablePos+1, newExpressionStmt);
        int newDiffLineIndex = getNewDiffLineIndex(diffLineIndex, changedStatement);

        generatedDate.generateSuccess = true;
        generatedDate.method = md.toString();
        generatedDate.diffLine = getNewDiffLine(md, newDiffLineIndex);
        generatedDate.diffLineIndex = String.valueOf(newDiffLineIndex);
        generatedDate.change = variableName + "->" + newName;

        return generatedDate;
    }

    @Override
    public String toString() {
        return this.getClass().getSimpleName();
    }

    public static void main(String[] args) throws IOException {
        String path = "F:\\workspace\\bug_detection\\data\\Dataset\\temp\\617925941f6e65eedfd3eef3.java";
        String txtCode = new String(Files.readAllBytes(Paths.get(path)));
        txtCode = "class T { \n" + txtCode + "\n}";
        CompilationUnit cu = StaticJavaParser.parse(txtCode);

        MethodDeclaration md = cu.findFirst(MethodDeclaration.class).get();
        String[] lines = md.toString().split("\n");
        System.out.println(lines[4]);
        NewVariable newVariable = new NewVariable();

        System.out.println();
    }
}
