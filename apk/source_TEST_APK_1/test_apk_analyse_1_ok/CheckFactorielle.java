package fr.univ.test_apk_analyse_1_ok;

public class CheckFactorielle {

    public static int factorielle(int n) {
        if(n == 0 || n == 1){
            return 1;
        }

        return n * factorielle(n - 1);
    }

    public static void check(){
        int[] facts = new int[5];

        for(int i = 0; i < facts.length; i++){
            facts[i] = factorielle(i);
        }
    }
}
