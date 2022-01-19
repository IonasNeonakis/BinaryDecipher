package fr.univ.test_apk_analyse_1_ok;

public class PalindromeCheckingService {

    public static boolean estPalindromeString(String mot){
        int i = 0;
        int longueur = mot.length() - 1;
        boolean egale = true;
        while(i < longueur/2 && egale){
            if(mot.charAt(i) == mot.charAt(longueur-i))
                egale = true;
            else
                egale = false;
            i++;
        }

        return egale;
    }

    public static boolean estPalindromeInt(int nombre) {
        if(nombre == inverse(nombre)){
            return true;
        }
        return false;
    }

    private static int inverse(int nombre){
        int inverse = 0;
        while(nombre != 0){
            inverse = inverse*10 + nombre%10;
            nombre = nombre/10;
        }
        return inverse;
    }
}
