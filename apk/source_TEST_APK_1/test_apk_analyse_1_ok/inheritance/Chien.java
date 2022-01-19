package fr.univ.test_apk_analyse_1_ok.inheritance;

public class Chien extends Canide {
    public Chien(){
        super();
        System.out.println("Bonjour depuis Chien");
    }

    public void bark(){
        super.genericSound();
        super.canideSound();
    }
}
