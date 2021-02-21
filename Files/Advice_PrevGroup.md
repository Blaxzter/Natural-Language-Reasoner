Hi all,

I'm from the group on explainable AI "from arguments to decisions" with Nico last semester. 

Our results can be found at 
https://explainable-reasoning.github.io/ . 

We ran out of time in the end, and I think the semantic tableaux prototype that is hosted there does not actually work, because we added some not-working code for a decision support system to it. (Both our approaches to the decision support system are not very satisfactory.) If you clone our repo and run the code for only the semantic tableaux, it should work, and there are lots of passing tests (at least for the tableaux part). Let me know if you have problems running the code. 

Some tips:
- We implemented the tableau with an actual tree structure with an object for each node. While this may be more intuitive, it is rather complicated and may lead to no longer relevant nodes remaining in memory rather than being garbage collected. It will be simpler to think of the tableau as a recursive function!
- If you need to use logic, don't waste time implementing logic from scratch like we did. Use/adapt pythological or something similar, or DePYsible for defeasible logic. NLTK also has libraries for logic 
http://www.nltk.org/howto/logic.html and 
http://www.nltk.org/howto/inference.html). Or use our implementation ;) 
- We made one prototype in Python and one (not using semantic tableaux, and not using much documentation, sorry) in Elm, a simple functional language compiling to websites. I found the second much more convenient. If you like an intro to Elm, I'm happy to give one. 
- Definitely check out these two papers for your project:
https://arxiv.org/abs/1708.09417 (with open source code!)
https://arxiv.org/abs/1711.06128 (with a nice dataset!)
- I have lists of conferences and companies in legal tech, if you are interested. 


Don't hesitate to send me questions!
Best wishes, David

