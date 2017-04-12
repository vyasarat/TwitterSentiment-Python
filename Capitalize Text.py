import re
import os

def replaceText(findThis,repThis):
        infile = open("export.sql", "r")
        outfile = open("TempOut.txt", "w")

        for line in infile:
                line.replace('\n','')
                src_str = re.compile(findThis, re.IGNORECASE)
                str_replaced = src_str.sub(repThis,line)
                outfile.write(str_replaced)

        infile.close()
        outfile.close()
        os.remove("export.sql")
        os.rename("TempOut.txt","export.sql")
        
def main():
        replaceText("EV Retail No Changes from previous","EV RETAIL NO CHANGES FROM PREVIOUS")
        replaceText("EV Retail Verification Full Verbal","EV RETAIL VERIFICATION FULL VERBAL")
        replaceText("EV Retail Via Domain Auth TAB or WHOIS Database","EV RETAIL VIA DOMAIN AUTH TAB OR WHOIS DATABASE")
        replaceText("EV Retail Via Domain Rights Verbal","EV RETAIL VIA DOMAIN RIGHTS VERBAL")
        replaceText("EV Retail Via Domain Rights via email","EV RETAIL VIA DOMAIN RIGHTS VIA EMAIL")
        replaceText("EV Retail With changes from previous","EV RETAIL WITH CHANGES FROM PREVIOUS")

        replaceText("OV Retail Replacement No Changes from previous","OV RETAIL REPLACEMENT NO CHANGES FROM PREVIOUS")
        replaceText("OV Retail Replacement with changes from previous","OV RETAIL REPLACEMENT WITH CHANGES FROM PREVIOUS")
        replaceText("OV Retail Verification Full Verbal","OV RETAIL VERIFICATION FULL VERBAL")
        replaceText("OV Retail Verification Online","OV RETAIL VERIFICATION ONLINE")
        
        replaceText("OV Retail Verification Previous Authentication","OV RETAIL VERIFICATION PREVIOUS AUTHENTICATION")
        replaceText("OV Retail Previous Verification","OV RETAIL VERIFICATION PREVIOUS AUTHENTICATION")

        replaceText("OV Retail Domain Auth TAB or WHOIS Database","OV RETAIL DOMAIN AUTH TAB OR WHOIS DATABASE")
        
        replaceText("OV Retail Via Domain Previous Authentication","OV RETAIL VIA DOMAIN PREVIOUS AUTHENTICATION")
        replaceText("OV Retail Domain Previous Authentication","OV RETAIL VIA DOMAIN PREVIOUS AUTHENTICATION")
        
        replaceText("OV Retail Via Domain Rights Verbal","OV RETAIL VIA DOMAIN RIGHTS VERBAL")
        replaceText("OV Retail Domain Rights Verbal","OV RETAIL VIA DOMAIN RIGHTS VERBAL")
        
        replaceText("OV Retail Via Domain Rights via email","OV RETAIL VIA DOMAIN RIGHTS VIA EMAIL")
        replaceText("OV Retail Domain Rights via email","OV RETAIL VIA DOMAIN RIGHTS VIA EMAIL")
        
        replaceText("OV Retail Via Domain rights via chat","OV RETAIL VIA DOMAIN RIGHTS VIA CHAT")
        replaceText("OV Retail Domain rights via chat","OV RETAIL VIA DOMAIN RIGHTS VIA CHAT")
        replaceText("good","GOOD")
main()
 
