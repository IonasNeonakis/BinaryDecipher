package fr.univ.test_apk_analyse_1_ok;

public class CheckSoManyParameters {

    public static String soManyParameters(String p1, String p2, String p3, String p4, String p5, String p6, String p7){
        return p1 + p2 + p3 + p4 + p5 + p6 + p7;
    }

    public static void check(){
        String res = soManyParameters("Bonjour", " je", " m'appelle", " Ezequiel", " Tournevis", " et", " non");
        System.out.println(res);
    }
}
