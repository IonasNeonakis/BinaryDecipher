package fr.univ.test_apk_analyse_1_ok;

public class CheckBoolArray {

    public static void check(int[] facts){
        boolean[] facts_even = new boolean[facts.length];

        for(int i = 0; i < facts_even.length; i++) {
            facts_even[i] = facts[i] % 2 == 0;
            if (facts_even[i]) {
                System.out.print("facts[" + i + "] = " + facts[i] + " et il est pair");
            }
        }
    }
}
