TEXT CLASSIFIER:

    the service read from elastic all the documents that still not classified(by bds_percent = -1)
    and calculating the hostile percent.
    the query also find the hostile words with the highlight parameter and with regex spliting the
    matched words to list to map every word if it hostile or not.

    then, calculating the hostile and not hostile percent by:

                        len(hostile/less_hostile words)/len(all_text):
                                to find the ratio between the hostile words to all the text
                                to decrease the percent in case that the len of the hostile is only one
                                and increase the percent when the hostile words is more common in the text to define more hostility

                                this happened each category word - hostile and less hostile
    
                        the_result_of_hostile * 2:
                                because of the rules to double the hostile percent

                        result_of_hostile + result_of_less_hostile:
                                because hostile and less hostile were founded - adding them

                        adding_result * score:
                                to see if the result i've got is realy like as its listed
                                to decrease the percent where the word founded were little distorted in the text or a combined with another word
                                and to increase the percent where the word founded excactly as it listed in the list

                        sum_percent * 100:
                                to see the percent in a comfortable format


    the classifier also calculating the is_bds true or false with a threshold of 40 because as it seems by the text,
    from 40 percent the text starting to be more hostility

    and calculating the risk_rank (none,medium,high) by binds of [0,40,80]:
            under 40 - its only talking
            over 40, under 80 - its more hostile
            over 80 - very hostile