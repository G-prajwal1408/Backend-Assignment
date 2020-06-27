import math, random 
import smtplib
from flask import Flask, render_template
def generateOTP() : 
    digits = "0123456789"
    otp = "" 
    for i in range(4) : 
        otp += digits[math.floor(random.random() * 10)]
    return otp
    