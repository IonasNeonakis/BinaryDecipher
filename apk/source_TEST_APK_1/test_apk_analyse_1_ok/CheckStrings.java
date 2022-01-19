package fr.univ.test_apk_analyse_1_ok;

public class CheckStrings {
    public static void check(){
        String test_string = "Bonjour";

        if(PalindromeCheckingService.estPalindromeInt(121)){
            System.out.printf("121 est un palindrome !");
        }else{
            System.out.println("C'est pas un palindrome !");
        }

        if(PalindromeCheckingService.estPalindromeString(test_string)){
            System.out.println(test_string + " est un palindrome !");
        }else{
            System.out.println("C'est pas un palindrome !");
        }

        if(PalindromeCheckingService.estPalindromeString("kayak")){
            System.out.println("Kayak est un palindrome !");
        }else{
            System.out.println("C'est pas un palindrome !");
        }
    }
}
