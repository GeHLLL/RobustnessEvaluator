package metamorphic;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Modifier;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.AnnotationExpr;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.expr.VariableDeclarationExpr;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.ExpressionStmt;
import com.github.javaparser.ast.stmt.Statement;
import com.sun.deploy.util.StringUtils;


import java.io.IOException;
import java.lang.annotation.Annotation;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class UnusedStatement extends Generator{
    private static Statement getUnusedStatement(){
        String timestamp = new Timestamp(System.currentTimeMillis()).toString();
        String unusedStr = "String timestamp = \"" + timestamp + "\";";
        return StaticJavaParser.parseStatement(unusedStr);
    }


    @Override
    public GeneratedDate generate(MethodDeclaration md, String diffLine, String buggyLineIndex) {
        //String[0] Change String[1] Method String[2] LineIndex
        //String[] res = new String[3];
        GeneratedDate generatedDate = new GeneratedDate();

        List<SimpleName> simpleNames = md.findAll(SimpleName.class);
        List<String> simpleNameStrings = new ArrayList<>();
        for (SimpleName simpleName: simpleNames){
            simpleNameStrings.add(simpleName.getIdentifier());
        }
        if(simpleNameStrings.contains("timestamp")) return generatedDate;


        Statement unusedStmt = getUnusedStatement();

        int statementNumber = md.getBody().get().getStatements().size();
        md.getBody().get().addStatement(new Random().nextInt(statementNumber+1), unusedStmt);

        String method = md.toString();
        String[] methodLines = method.split("\n");
        int diffLineIndex = -1;
        for(int i=0;i<methodLines.length;i++){
            String line = methodLines[i];
            line = line.trim();
            diffLine = diffLine.trim();
            if(line.equals(diffLine)){
                diffLineIndex = i;
                break;
            }
        }
        if(diffLineIndex == -1) return generatedDate;

        generatedDate.change = unusedStmt.toString();
        generatedDate.diffLineIndex = String.valueOf(diffLineIndex);
        generatedDate.diffLine = methodLines[diffLineIndex];
        generatedDate.method = md.toString();
        generatedDate.generateSuccess = true;

        return generatedDate;

    }



    @Override
    public String toString() {
        return "UnusedStatement";
    }

    public static void main(String[] args) throws IOException {
        String path = "F:\\workspace\\bug_detection\\data\\Dataset\\temp\\617925941f6e65eedfd3eef3.java";
        String txtCode = new String(Files.readAllBytes(Paths.get(path)));
        txtCode = "class T { \n" + txtCode + "\n}";
        System.out.println(txtCode);

        CompilationUnit cu = StaticJavaParser.parse(txtCode);

        BlockStmt blockStmt = new BlockStmt();
        List<Statement> statements = cu.clone().findFirst(MethodDeclaration.class)
                .flatMap(MethodDeclaration::getBody).get().getStatements();

        for(int i=0;i<statements.size();i++){
            if(statements.get(i).isExpressionStmt()){
                System.out.println(statements.get(i).hashCode());
                ExpressionStmt expressionStmt = (ExpressionStmt)statements.get(i);
                System.out.println(expressionStmt.hashCode());
                if(expressionStmt.getExpression().isVariableDeclarationExpr()){
                    VariableDeclarationExpr variableDeclarationExpr = expressionStmt.getExpression().asVariableDeclarationExpr();


                }
            }
        }


        System.out.println(blockStmt.toString());
        Statement unusedStmt = getUnusedStatement();
        blockStmt.addStatement(0, unusedStmt);
        List<Statement> statements1 = cu.findFirst(MethodDeclaration.class).get().getBody().get().getStatements();
        cu.findFirst(MethodDeclaration.class).get().getBody().get().addStatement(1, unusedStmt);
        System.out.println(cu.toString());

        for(int i=0;i<10;i++){
            System.out.println(new Random().nextInt(1));
        }
    }
}
