package metamorphic;

import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class NameAnalysis {

    public List<String> camelCaseAnalysis(String name){
        assert name.length() >= 0;
        List<Integer> posList = new ArrayList<>();
        if(Character.isLowerCase(name.charAt(0))) {
            name = Character.toUpperCase(name.charAt(0)) + name.substring(1);
        }

        for(int i=0;i<name.length();i++){
            if(Character.isUpperCase(name.charAt(i))){
                posList.add(i);
            }
        }
        posList.add(name.length());

        List<String> wordList = new ArrayList<>();

        for(int i=0;i<posList.size()-1;i++){
            wordList.add(name.substring(posList.get(i), posList.get(i+1)));
        }

        return wordList;
    }


    public List<String> getNameList(String rawName){
        List<String> nameList = new ArrayList<>();
        if(!(rawName.indexOf("[]")==-1)){
            while(!(rawName.indexOf("[]")==-1)){
                rawName = rawName.replace("[]", "");
            }
            rawName = rawName + "Array";
        }
        String mapRegex = ".*?<.*?,.*?>$";
        if(rawName.matches(mapRegex)) return nameList;

        String listRegex = "<.*?>";
        Pattern listPattern = Pattern.compile(listRegex);
        Matcher matcher = listPattern.matcher(rawName);
        List<String> matchedList = new ArrayList<>();
        while(matcher.find()) matchedList.add(matcher.group());
        if(matchedList.size()>1) return nameList;
        if(matchedList.size()==1){
            String str = matchedList.get(0);
            rawName = rawName.replace(str, "");
            rawName = str.substring(1, str.length()-1) + rawName;
        }

        List<String> words = camelCaseAnalysis(rawName);

        //1.
        StringBuilder sb1 = new StringBuilder();
        StringBuilder sb2 = new StringBuilder();
        StringBuilder sb3 = new StringBuilder();
        StringBuilder sb4 = new StringBuilder();
        for(int i=0;i<words.size();i++){
            String word = words.get(i);
            if(i==0){
                word = Character.toLowerCase(word.charAt(0)) + word.substring(1);
                sb3.append(word.charAt(0));
            }
            sb1.append(word);
            sb2.append(Character.toLowerCase(word.charAt(0)));

            if(i==words.size()-1){
                sb4.append(Character.toLowerCase(word.charAt(0)) + word.substring(1));
            }
        }
        nameList.add(sb1.toString());
        nameList.add(sb2.toString());
        nameList.add(sb3.toString());
        nameList.add(sb4.toString());

        return nameList;
    }
    public static void main(String[] args) {
        NameAnalysis nameAnalysis = new NameAnalysis();
        List<String> list = nameAnalysis.getNameList("List<Integer>");
        for(String name: list){
            System.out.println(name);
        }
    }
}
