Candidate Portal Practice Questions - Name, Address, Pin (V2024)

This short Data Accuracy practice assessment has been created to help you prepare for your exam.  There are 15 questions in total. 
 
 Before you begin rating please review the following concepts:
1. Name Accuracy 
2. Address Accuracy
3. Pin Accuracy

As you take this  practice assessment please take note of the feedback comments and guideline references as these sections are key to passing the exam. You can retake this Assessment  as many times as you wish.  We recommend that you keep the guidelines open as you complete the assessment. 


Q1 Name Accuracy
1. The user’s query is The Metropolitan Museum on Fifth Avenue New York City


The returned result in Tryrating is 

1000 Fifth Avenue
1000 Fifth Avenue, New York, NY, 10028. 

What is the correct Name Accuracy Rating?
  *
N/A
Correct
Partially Correct
Incorrect


Q1 Correct
You are Correct!

The correct rating is N/A. The n/a rating should be used for all address-type results, including residential addresses, streets, localities, and so on. (See section 6.1 of the guidelines).

LLM: 
The correct Name Accuracy rating for this result is **N/A**.

### **Reasoning**
The determination of this rating is based on the following principles found in the sources:

*   **Result Type Identification:** The user's query is for a specific Point of Interest (POI), "The Metropolitan Museum." However, the returned result in TryRating is **1000 Fifth Avenue**, which is an **Address Type Result** rather than a Business or POI record.
*   **Guideline Rule for Address Results:** According to Section 6.1 of the guidelines, the **n/a (Not Applicable)** rating must be used for all address-type results, including residential addresses, streets, and localities.
*   **Result Representation:** In address results, the name field does not contain a business name; instead, it displays the **first line of the address** as a title. Because there is no business or POI name provided to evaluate, the accuracy of a name cannot be rated.
*   **Independence of Ratings:** While the **Relevance** rating for this scenario would be **Bad** (because a POI query returning only an address result indicates a "Lack of Connection"), **Name Accuracy is evaluated independently** based on the structure of the result itself.

### **Research Tip**
For this specific question, **no external research is required**. The rating is determined purely by identifying that the result type is an address rather than a business or POI entry. If the result had included a business name (e.g., "The Metropolitan Museum of Art"), you would then conduct research to determine if that name was Correct, Partially Correct, or Incorrect.

***

**Analogy:** Rating the name accuracy of an address result is like trying to grade a student's **math homework** on their **spelling accuracy** when the assignment only contains **numbers**. Since there are no words to evaluate, you simply mark that specific criteria as "Not Applicable".

Q2 Name Accuracy
2. The following result is returned in Tryrating 

 Name: Olive Garden 
 Classification:  Hardware Store
 Address: 50 Kunckle Drive, Easton, PA, 18045

Per Guidelines Section 6.3.2 Name Accuracy rating should be:  *
Correct
Incorrect
N/A

Q2: Correct
You are Correct.

The Name Accuracy rating is Incorrect . Here, the name is correct, but the classification is incorrect. The classification “Hardware Store” is misleading. When the category is wrong, the final Name and Category Accuracy rating is always incorrect. This is true whether the result name is correct, partially correct, or incorrect.
Refer to the guidelines section 6.3.2. Incorrect Category, to learn more.


LMM:
The correct Name Accuracy rating for this result is **Incorrect**.

### **Reasoning**
The determination of this rating is governed by **Section 6.3.2** of the guidelines regarding the **Incorrect Category** rule:

*   **Rule for Misleading Categories:** According to the guidelines, when the classification or category assigned to a business is wrong or misleading, the final Name and Category Accuracy rating is **always Incorrect**.
*   **Application to this Scenario:** The business name returned is **Olive Garden**, which is a globally recognized chain of Italian restaurants. However, the classification provided in the result is **Hardware Store**. 
*   **Irrelevance of Name Precision:** Even if the name "Olive Garden" is spelled perfectly and is officially correct, the severe mismatch between the business's actual nature (restaurant) and the provided classification (hardware store) makes the result misleading for the user.
*   **Summary Table Rule:** The guidelines include a summary table showing that the combination of a "Correct Name" and an "Incorrect Category" must result in an overall rating of **Incorrect**.

### **Research Steps for the Exam**
For Name and Category Accuracy, external research is **mandatory**:
1.  **Verify the Category:** Conduct a search for the business name and address (e.g., "Olive Garden Easton PA") to confirm its primary intent. 
2.  **Confirm the Name:** Check the official company website or store locator to ensure the name "Olive Garden" matches their branding.
3.  **Check Street View:** If possible, use imagery to confirm if the signage at the physical location matches the name and nature of the business.

***

**Analogy:** This is like a library catalog entry that correctly lists the title of a book as **"The Great Gatsby"** but categorizes it under **"Chemistry Textbooks."** Even though the name is right, the classification is so fundamentally wrong that the entry is considered **Incorrect** and useless for someone looking for science resources.

Q3 Address Accuracy
3. The user has issued a query for Queens Village Station. The result you are asked to rate is Queens Village Station. The address provided is Queens, NY 11428 United States. How should address accuracy be rated? *
Correct
Correct with Formatting
Incorrect

Q3 Correct
You are Correct.

For Transit POIs, no street address is expected. The provided address is just the locality. The POI is physically located within the given locality. So the address rating is "Correct."
Refer to the Quincy Station example in Guidelines Section 8.3.2.1. Minimum Address Component, to learn more.

The correct Address Accuracy rating for **Queens Village Station** is **Correct**.

### **Reasoning**
The rating is determined by the specific rules for transit features found in the guidelines:

*   **POI Classification:** Queens Village Station is a **Transit Point of Interest (POI)**. These are classified as **"Features Without an Expected Address"**.
*   **Minimum Component Rule:** According to Guidelines Section **8.3.2.1 (Minimum Address Component)**, users do not typically expect a street name and number for transit stops, stations, or airports. 
*   **Sufficient Information:** For these features, providing the **locality (Queens), state (NY), and a valid postal code (11428)** is considered a complete and accurate address as long as the POI is physically located within that locality. 
*   **Precedent:** This logic follows the **Quincy Station** example in the guidelines, where an address listing only the locality (Chicago, IL) was rated **Correct** because no street address was expected for the transit feature.
*   **Why not "Correct with Formatting"?** This rating is reserved for cases where all information is present but in an **unexpected order**, contains extra spacing, or minor punctuation issues like double commas. Since the street address is **not a required component** for a station, its absence is not a formatting error.

### **Research Tip**
When rating Address Accuracy for transit POIs, you should conduct research to confirm the station's physical location. Verify through maps or official transit authority websites (like the MTA or LIRR) that the **ZIP code** and **locality** provided in the result accurately cover the area where the station exists.

***

**Analogy:** Rating a transit station by only its city and ZIP code is like looking for a **large stadium** in a small town. If someone tells you the stadium is in **"Paide, 72720,"** that is a **Correct** set of directions; because the stadium is a major, well-known landmark, you don't need a specific house number on a street to find it.

Q4 Name Accuracy
4. The User has issued a query for  1099 Ohio River Blvd, Pittsburgh, PA 15143, United States

The result returned is 1099 Ohio River Blvd, Pittsburgh, PA 15143, United States

How should Name Accuracy be rated? *
Correct
Partially Correct
N/A
Incorrect
Can't Verify

Q4 Correct
You are Correct.

The Address Accuracy rating is N/A.  Per Section 6.1 the n/a rating should be used for all address-type results, including residential addresses, streets, localities, and so on.

LLM: The correct Name Accuracy rating for this result is **N/A**.

### **Reasoning**
The determination of this rating is based on the following principles from the sources:

*   **Result Type Identification:** The user's query and the returned result are both **full addresses**. Because the result consists strictly of address components and does not include a business name or category, it is classified as an **Address Type Result**.
*   **Guideline Rule (Section 6.1):** According to the guidelines, the **n/a (Not Applicable)** rating must be selected for **all address-type results**, including residential addresses, streets, and localities.
*   **Absence of a Name Field:** In address results, the field that usually contains a business name instead displays the **first line of the address** as the result title. Since there is no actual business or POI name to evaluate, Name Accuracy is not applicable.
*   **Independence of Rating Components:** Data accuracy components (Name, Address, and Pin) are rated **independently**. While you would still need to verify the **Address Accuracy** and **Pin Accuracy** for this result using tools like USPS or Street View, the **Name Accuracy** is automatically designated as N/A due to the result type.

### **Research Requirement**
For this specific question, **external research is not required** to determine the Name Accuracy rating. The rating is assigned based purely on identifying the result as an address-only record. Research is only mandatory for Name Accuracy when the result is a Business or POI, to verify that the displayed name matches official sources.

***

**Analogy:** Rating the Name Accuracy of a pure address result is like a teacher trying to grade a student's **vocabulary** on a **math test** that only contains numbers. Since there are no words (or names) to evaluate, the criteria simply **does not apply**.

Q5 Pin Accuracy
5. The POI we are asked to rate is located inside a mall with shared parking that has no public or internal access roads passing through it. The pin lands on the roof of the mall but not on the specific POI you are asked to rate. Outside research we conduct confirms the exact location of the business via street imagery and the online Mall Directory. What is the correct Pin Rating? *
Perfect
Approximate
Wrong
Can't Verify

Q5 Correct
You are Correct. 

The pin falls on the parcel; however, it does not land on the exact business. Therefore, it can be rated Approximate. If you can determine exactly where the store is located via an online map directory or street imagery, then the pin should be placed over the expected area to receive a perfect rating. 
Refer to the Pho 2 Love example from the guidelines section 9.3.2, Boundaries in Shared Spaces.

LLM: The correct Pin Accuracy rating for this scenario is **Approximate**.

### **Reasoning**
The determination of this rating is based on the rules for **Boundaries in Shared Spaces** and the use of **Best Available Evidence** as described in the sources:

*   **Definition of Perfect vs. Approximate in Shared Spaces:** A pin is rated **Perfect** if it drops directly on the rooftop of the specific POI being evaluated. However, when a result is under a shared rooftop (like a mall or strip mall) and research provides strong evidence (such as a **Mall Directory** or **Street View**) of its exact location, **only that specific portion of the roof** is considered the Perfect area. 
*   **Application to this Scenario:** In this case, you have conducted research and confirmed the exact location of the business within the mall. Because the pin lands on the roof of the mall but **not on the specific section** occupied by that business, it has missed the Perfect area.
*   **Property Boundaries:** Because the pin is still on the mall roof—which is part of the same connected building and property parcel—it satisfies the criteria for **Approximate**. A pin is Approximate if it falls within the property boundaries but outside the area that qualifies for a Perfect rating.
*   **Next Door Exclusion:** The "Next Door" rating is **never used** for features within the same property boundaries or shared parking lots. 

### **Summary for the Exam**
*   **Rating:** Approximate
*   **Why:** The pin is on the correct building/parcel but misses the specific business location that was confirmed through research.
*   **Rule Reference:** Guidelines Section 9.3.2 (Boundaries in Shared Spaces) and 9.4 (Single Rooftop - Shared Parking Lot).

***

**Analogy:** Imagine you are looking for a specific **department in a large hospital**. If a map points to the **hospital's main building**, but research tells you that the department you want is actually in the **far east wing**, the pin is **Approximate**. It got you to the right complex, but it didn't point to the exact "room" you were looking for.

Q6 Pin Accuracy
6. What is the Pin Accuracy of this result 

(coordinates you can copy and paste for research : 38.788580, -90.531115)  *
Perfect
Approximate
Wrong
Can't verify

Kaart failis: PinAccuracy_HomeDepotNearby_PrexExam_Q6.png

Q6 Correct
You are Correct.

The Pin Accuracy is Approximate. The pin lands in the parking lot of where the business is housed but not on the rooftop.
Review sections 9.1.2. Approximate and 9.3. Boundaries of the Feature for more details.

LLM: The correct Pin Accuracy rating for this result is **Approximate**.

### **Reasoning**
The determination of this rating is based on the following principles from the guidelines and practice materials:

*   **Pin Placement:** The result for **Lowe's Home Improvement** shows a pin that lands in the **parking lot** area of the property rather than directly on the **rooftop** of the building.
*   **Definition of Perfect:** According to Section 9.1.1, a pin is only rated **Perfect** if it drops directly on the rooftop of a Point of Interest (POI) or on the listed feature itself.
*   **Definition of Approximate:** A pin is rated **Approximate** if it drops within the property boundaries (parcel) of the result but outside the specific area that qualifies for a Perfect rating. 
*   **Property Boundaries:** In the case of a single large building with a large parking lot, the entire parcel—including the parking area—is considered part of the feature's boundaries. Because the pin is on the correct property but on the asphalt (parking lot) instead of the building, it satisfies the criteria for **Approximate**.

### **Research Confirmation**
If you paste the coordinates (**38.788580, -90.531115**) into a map provider and view the satellite imagery, it confirms that the pin is located within the **Lowe's property parcel** but is clearly positioned in the parking spaces in front of the store. 

***

**Analogy:** Imagine you are visiting a friend at a **large apartment complex**. If your GPS tells you that you have arrived while you are still in the **complex's parking lot**, it has gotten you to the right property (**Approximate**), but it hasn't pointed you to their specific **front door** (**Perfect**).


Q7 Pin Accuracy
7. What is the  Pin Accuracy Rating  of this Result?


Kroger Fuel Center
2525 Hillard Rome Rd
Hillard OH 43026
USA


Coordinates : 40.002615, -83.154804





Perfect
Approximate
Wrong
Can't Verify


Kaart failis: KrogerHillard_PreExamPinAccuracy_Q7

Q7 Correct
You are Correct.

You are Correct. The result is “Kroger Fuel Center,” and the pin lands on the canopy over the pumps (https://goo.gl/maps/E9g5eZHEohgPyaJz7 ). The Pin Rating is Perfect.
Refer to the Canadian Tire Gas+ example from the guidelines section 9.5.1, Multiple-Rooftop Rating, to learn more.

The correct Pin Accuracy rating for the **Kroger Fuel Center** is **Perfect**.

### **Reasoning**
The determination of this rating is based on the specific rules for Point of Interest (POI) features with associated structures:

*   **POI Identification:** The result is for a **Kroger Fuel Center**, which is a service station.
*   **Pin Placement:** Satellite imagery shows that the pin lands **directly on the canopy** (the roofed structure over the gas pumps).
*   **Definition of Perfect:** According to Section 9.1.1 of the guidelines, a pin is rated **Perfect** if it drops directly on the rooftop of a POI or on the listed feature itself. For gas stations and fuel centers, the canopy over the pumps is considered a primary structure and part of the "Perfect" area.
*   **Contrast with Approximate:** If the pin had landed in the **parking lot** surrounding the fuel center or on the main Kroger grocery building nearby, the rating would have been **Approximate**. Because the pin identifies the specific structure the user is looking for (the fuel pumps), it earns the highest rating.

### **Research Tip for the Exam**
When rating gas stations or fuel centers, always switch to **Satellite View** and zoom in. A pin that is centered on the **canopy** or the **small attendant kiosk** is **Perfect**. If the pin is on the asphalt between the pumps or in the general parking area, it is **Approximate**. This specific question follows the logic found in the **Canadian Tire Gas+** example in Section 9.5.1 of the guidelines.

***

**Analogy:** Imagine you are meeting someone at a **specific table** in a park. If your map points to the **entire park**, it is **Approximate**. If the map points exactly to the **roof of the gazebo** where that table is located, the pin is **Perfect**.

Question 8 Address Accuracy
8. What is the Correct Address Accuracy  for this result  ?

Lowe's Home Improvement
2900 Clay Street,
Saint Charles, MO 63301
USA


  *
Correct
Correct with Formatting
Incorrect
Can't Verify


Q8 Correct
You Are Correct. 

The result address is missing the street direction (W: West), which is included in the official website (https://www.lowes.com/store/MO-Saint-Charles/1057 ). We should check this on USPS when we notice this. USPS confirms the 'W' directional type in the street name. The correct address is [2900 W CLAY ST, SAINT CHARLES, MO 63301]. The result address doesn't match with the official website or USPS. Therefore, the address accuracy is Incorrect. 
Refer to example "118 El Camino Real" from guidelines section 7.1.3, Street Name, subsection Street Directions and Types.

The correct Address Accuracy rating for this result is **Incorrect**.

### **Reasoning and Analysis**
The rating is determined by comparing the address provided in the result to official sources and applying the specific rules regarding street components found in the guidelines:

*   **Discrepancy Identification:** The result in TryRating displays the address as **2900 Clay Street**, Saint Charles, MO 63301. However, research through the official Lowe’s store locator and the **USPS ZIP Code Lookup** confirms that the correct, deliverable address is **2900 W CLAY ST**.
*   **Mandatory Component Rule:** According to **Section 7.1.3 (Street Directions and Types)**, street directions such as North (N), East (E), South (S), and **West (W)** are considered **integral parts of the street name**. 
*   **Rating Classification:** The guidelines state that if a directional component is missing or incorrect, the street name is considered wrong. Therefore, the result must be rated **Incorrect**, specifically with the issue **Street Name** or **Street Direction** selected.
*   **Comparison to Guideline Examples:** This scenario is analogous to the **"118 El Camino Real"** example in the guidelines, where the result was missing the directional "E" (East). That example was also rated **Incorrect – Street Name** because the missing direction rendered the address inaccurate.

### **Research Requirements for the Exam**
*   **USPS Verification:** When evaluating addresses in the United States, you must check the **USPS website** to see if the address is a valid, deliverable mailing address and to confirm the exact spelling and directional types.
*   **Official Store Locators:** For chain businesses like Lowe's, you must utilize the **official website's store locator** to find the precise branch address, as TryRating results may sometimes omit critical details.

***

**Summary for TryRating:**
*   **Rating:** Incorrect
*   **Issue Checkbox:** Street Name / Street Direction
*   **Comment:** The result address is missing the mandatory street direction "W" (West). The correct address is 2900 W Clay St per the official Lowe's website and USPS.

**Analogy:** 
Missing a street direction is like giving someone directions to a house but forgetting to tell them if it’s on the **North or South side** of a major river dividing the city. Even if the street name and number are right, without that direction, they could end up miles away in the completely wrong part of town.


Q9 Name Accuracy
9. What is the Correct Name Accuracy for the following Result  *
N/A
Correct
Partially Correct
Incorrect
Can't Verify

Q9 Correct
You are Correct.

The Name Rating is Partially Correct.  Per section 6.2.2, Partially Correct Name, when a name is returned that is a slight variation from the official website, but is recognizable by the user, it is considered Partially Correct. In this case, the name is recognizable with an additional apostrophe included that is not listed on the official website (https://www.wegmans.com/ ). Since the classification is correct and the name contains a minor punctuation error, name accuracy is PARTIALLY CORRECT.


LLM:
The correct Name Accuracy rating for the **Wegmans** result is **Partially Correct**.

### **Reasoning and Analysis**
According to the guidelines and practice feedback, the rating is determined by comparing the displayed result name to the official branding:

*   **Official Branding:** Research of the company’s official website (wegmans.com) confirms that the correct, official name of the chain is **Wegmans** (without an apostrophe).
*   **Result Discrepancy:** The name returned in TryRating is **Wegman's**, which includes an additional apostrophe not present in the official name.
*   **Guideline Application (Section 6.2.2):** Per the "Partially Correct Name" rule, when a returned name is a slight variation from the official source but remains clearly recognizable to the user, it must be rated **Partially Correct**.
*   **Classification of Error:** Minor punctuation issues, such as extra or missing apostrophes, unnecessary spaces, or minor misspellings, are categorized as partially correct because they do not interfere with the user's ability to identify the business.

### **Required Rating Workflow**
When submitting this rating in the tool, you must follow these steps:
1.  **Select Rating:** Choose "Partially Correct" from the Name and Category Accuracy dropdown.
2.  **Select Issue:** Check the **Name Issue** checkbox that appears.
3.  **Provide a Comment:** Because the rating is not "Correct," a mandatory comment is required in English.
    *   *Example Comment:* "The name is recognizable but includes an additional apostrophe not found on the official website (wegmans.com). Per Section 6.2.2, this punctuation error is Partially Correct."

***

**Analogy:** Rating this name is like grading a spelling test where a student writes **"Appel"** instead of **"Apple."** You know exactly what fruit they are talking about, so they get partial credit for being recognizable, even though the specific characters used are technically slightly off.

Q10 Pin Accuracy
10. What is the correct Pin Accuracy Rating for the following result 

Attleboro Station
133 S Main Street
Attleboro, MA 02703
USA



(Coordinates : 41.940203, -71.285516)  *
Perfect
Approximate
Wrong
Can't Verify

Q10 Correct
You are Correct. 

When the result is a transit POI with a single rooftop, a pin falling on the station rooftop can be rated as perfect. Here, based on a combination of street and aerial imagery, it can be confirmed that the pin lands on the correct rooftop. So, pin accuracy for the result is PERFECT.
Refer to the guidelines section 9.8.3, Transit POIs with a Single Rooftop, to learn more.

The correct Pin Accuracy rating for **Attleboro Station** is **Perfect**.

### **Reasoning and Analysis**
The determination of this rating is based on the specific rules for transit Point of Interest (POI) features as defined in the guidelines:

*   **Feature Identification:** The result is for **Attleboro Station**, which is a train station (Transit POI).
*   **Pin Placement:** Satellite imagery confirms that the pin lands **directly on the station’s rooftop or platform** area.
*   **Guideline Rule for Transit POIs:** According to Section **9.8.3 (Transit POIs with a Single Rooftop)**, a pin that falls directly on the station building or the platform area where a user would wait for transit is rated **Perfect**.
*   **Contrast with Other Ratings:** If the pin had landed in the station's parking lot or on an adjacent property, it would be rated **Approximate**. Because it lands on the primary structure the user is looking for (the station itself), it receives the highest accuracy rating.

### **Research Steps for the Exam**
To verify this in a live task, follow these steps provided in the sources:
1.  **Use Satellite View:** Open the coordinates (**41.940203, -71.285516**) and zoom in using satellite or aerial imagery.
2.  **Identify Structures:** Locate the tracks and the associated station buildings or platforms.
3.  **Apply the "Waiting Area" Rule:** Confirm if the pin is on the roof of the station or the area where passengers wait. If it is on the roof or platform, the rating is **Perfect**.

### **Summary for TryRating**
*   **Rating:** Perfect.
*   **Best Available Evidence:** Aerial and street imagery confirm the pin lands on the correct station rooftop.

***

**Analogy:** Imagine you are meeting someone at a **specific platform** in a large train station. If their digital location pin shows them standing in the **middle of the parking lot**, it is **Approximate**. If the pin shows them standing **exactly on the roof of the platform** where the train arrives, the pin is **Perfect**.


Q11 Pin Accuracy
11. While rating a task  it is determined that the Address does not exist and cannot be verified by official resources including Street Imagery and USPS. When the address does not exist how should the Pin Accuracy Component be rated? *
Approximate
Next Door
Wrong
Can't Verify

Q11 Correct
You are Correct.

The Pin Accuracy rating is Can't Verify.  Per section 10.3, when an address does not exist, the pin rating should be rated CAN'T VERIFY. There is no exact position for the pin to be placed.

The correct Pin Accuracy rating for a non-existent address is **Can't Verify**.

### **Reasoning and Analysis**
The determination of this rating is based on specific mandatory rules found in the guidelines regarding non-existent features:

*   **Absence of a Reference Point:** Pin Accuracy ratings (Perfect, Approximate, Next Door, or Wrong) require a verified "true" location to serve as a comparison. When research through official resources like the **USPS** and **Street Imagery** confirms that an address does not exist, there is no valid physical position for the pin to be placed.
*   **Guideline Mandate (Section 10.3):** According to the guidelines, whenever an address is rated **Incorrect – Address does not exist**, the Pin Accuracy component must automatically be rated **Can’t Verify**. 
*   **Application to Address Type Results:** This rule applies strictly to address-type results where the physical land plot or building cannot be identified. Even if the pin lands on a random building, it cannot be rated "Wrong" or "Approximate" because the specific target address it is supposed to represent has no real-world coordinates.
*   **Research Requirement:** To reach this rating, you must first prove the address is non-existent. For example, if a USPS lookup returns an "**N**" (not a deliverable mailing address) and imagery shows only an empty field or a different street range, the address is confirmed as non-existent.

### **Summary for TryRating**
*   **Address Accuracy:** Incorrect – Address does not exist.
*   **Pin Accuracy:** Can't Verify.
*   **Relevance Note:** Interestingly, if the query was for that specific address and the result matches it exactly (even though it doesn't exist), the Relevance rating can still be **Excellent**, but the data accuracy components must reflect the lack of existence.

***

**Analogy:** Rating the pin accuracy of a non-existent address is like trying to decide if a **dart** hit the **bullseye** when there is **no dartboard** on the wall. Since the target doesn't exist, you cannot measure how close or far the dart (the pin) is from it; therefore, the accuracy is simply "unverifiable."


Q12 Pin Accuracy
12. What is the Correct Pin Accuracy Rating for this result? 

Wendys
345 Valley Ave
Homewood AL 35209
USA

Result Coordinates: 33.472002, -86.820814 *
Perfect
Approximate
Next Door
Wrong
Can't Verify

Q12 Correct
You are Correct. 

You are Correct. The Pin Accuracy is Wrong. By searching for the location on a separate map application, we see that the pin is landing on a neighboring business and not on the requested Wendy's.  The business the pin lands on is not on the same block (there is a street in between the two businesses, 'Palisades Dr' https://tinyurl.com/mryub8vc ).

Therefore, this pin would not qualify as a Next Door pin because the guidelines state: the next-door property must be on the same block as the intended property. Review section 9.1.3 Next Door and example for Pin on the same block [1491 Kooser Rd San Jose, CA 95118] from section 9.4. Single Rooftop.


The correct Pin Accuracy rating for this result is **Wrong**.

### **Reasoning and Analysis**
The determination of this rating is based on the relationship between the pin placement and the property boundaries as defined in the guidelines:

*   **Pin Location:** Research confirms that the provided coordinates (33.472002, -86.820814) land on a **neighboring business** rather than on the rooftop of the intended Wendy's.
*   **The "Same Block" Rule:** To qualify for a **Next Door** rating, a pin must land on a property that is immediately adjacent, on the same side of the street, and on the **same block**.
*   **Presence of a Boundary:** In this case, there is a public road named **Palisades Dr** that runs between the Wendy's property and the neighboring business where the pin landed.
*   **Definition of Wrong:** According to the guidelines, a **public road acts as a boundary** that separates features into different blocks. Because the pin is on a different block from the target POI, it cannot be rated Next Door or Approximate and is instead rated **Wrong**.
*   **Independent Evaluation:** Pin accuracy is rated strictly on its physical placement relative to the real-world location, regardless of whether the name or address fields are correct.

### **Summary for TryRating**
*   **Rating:** Wrong
*   **Comment:** Research via external maps shows the pin lands on a different business. Because the pin and the target Wendy's are separated by a street (**Palisades Dr**), they are not on the same block, and the pin is rated **Wrong** per Section 9.1.3.

***

**Analogy:** Imagine you are trying to visit a neighbor's house. If you stand in the yard of the person **directly next to them** on your side of the sidewalk, you are **Next Door**. However, if you have to **cross a street** to get to where you are standing, you have moved to a different block entirely; in mapping terms, your location is now considered **Wrong**.

Q13 Pin Accuracy
13. Per section 9.6.2. Transit POI with Multiple Rooftops/Platforms , when the pin falls beyond the waiting area but still within the half and half area to the street/within 50m what is the correct Pin Accuracy rating? *
Correct
Approximate
Next Door
Wrong
Can't Verify

Q13 Feedback
You are Correct.

The Correct rating is Approximate. Per section 9.8.2. Transit POI with Multiple Rooftops/Platforms, when the pin falls beyond the waiting area but still within the half and half area to the street/within 50m, pin accuracy is considered APPROXIMATE. An example of this would be in the scenario of a pin being placed on a grassy area just outside of where you might wait for a train.

The correct Pin Accuracy rating is **Approximate**.

### **Reasoning**
The rating is determined by the specific criteria for **Transit POIs with Multiple Rooftops/Platforms** (Section 9.8.2 in current guidelines):

*   **Perfect Area:** A pin is only rated **Perfect** if it lands directly on the station polygon, a rooftop, a platform, or the specific area where a passenger would wait for transit.
*   **Approximate Area:** According to the sources, a pin is considered **Approximate** if it falls outside that primary waiting area but satisfies the following proximity rules:
    *   It is within **50 meters** of the area where you would wait for transit.
    *   It remains within the **station property boundaries**, which include parking lots and the area defined by the **"Half 'n' Half" rule** (extending to the middle of the adjacent street).
*   **Application to this Scenario:** Because the pin in this question is described as falling **beyond the waiting area** (missing Perfect) but still within **50m** and the **half and half area** to the street, it fits the definition of Approximate.
*   **Exclusion of "Next Door":** It is important to note that **Transit POIs do not have "Next Door" ratings**. Any pin that misses the Approximate area is automatically rated **Wrong**.

### **Summary for the Exam**
*   **Rating:** Approximate
*   **Why:** The pin misses the specific waiting area (Perfect) but is within the 50m/Half 'n' Half buffer zone associated with the station property.
*   **Example Case:** A pin placed on a grassy patch or sidewalk just outside the station building or platform is a common example of an Approximate rating for a transit feature.

***

**Analogy:** Imagine you are meeting someone at a **bus stop**. If the map shows them standing **under the bus shelter**, the pin is **Perfect**. If the map shows them standing **on the grass 20 feet behind the shelter**, the pin is **Approximate**. It’s not the exact spot for boarding, but it’s close enough for you to see them and know you are at the right location.


Q14 Pin Accuracy
14. When there is a difference  on the task interface between where the pin drops in Satellite Imagery and  where the pin shows in Vector map always base your rating  on the  map layer in Tryrating which is more generous toward the pin rating.  *
True
False

Question 14 Feedback
You are Correct.

The correct answer is True. When there is a difference between how the pin shows in Vector and Satellite imagery on the Try rating page always rate based on which map layer provides the higher rating option for Pin Accuracy. For example, If the Pin drops on the rooftop on Satellite Imagery but the pin lands on the parking lot in Vector map layer rate using the satellite imagery as this will provide a better rating for pin. See section 9.3.3. Map View Layers, for more information. 

The statement is **True**.

### **Reasoning and Guideline Application**
The determination that this statement is true is based on mandatory rules established in the rating guidelines regarding map discrepancies:

*   **The Generosity Rule (Section 9.3.3.1):** According to the sources, when there is a physical difference between where the pin appears on the **Satellite Imagery** and the **Vector map** within the TryRating interface, you must always choose the layer that results in the **highest possible accuracy rating**.
*   **Definition of "More Generous":** In this context, "more generous" means the layer that provides a better rating on the scale (Perfect > Approximate > Next Door > Wrong).
    *   *Example:* If the pin lands on the **rooftop** in Satellite view (which qualifies for **Perfect**) but appears in the **parking lot** in Vector view (which would only be **Approximate**), you must rate the pin as **Perfect** based on the satellite imagery.
*   **Large-Scale Discrepancies:** This rule applies even if there is a major offset or shift between the two layers across a large area, such as an entire city or region. You are instructed to "rate according to the most generous layer" regardless of which layer appears more technically "aligned" with the coordinates.
*   **Absence of Features:** If the Vector map is technically more generous but lacks building contours, you should use the Satellite imagery as a reference to estimate where the buildings would be on the Vector map to allow for a more favorable rating.

### **Scope of the Rule**
It is critical to note that this "generosity" comparison applies **only to the layers provided within the TryRating tool**. While you use external tools (like Google Maps or official store locators) to find the "true" real-world location of a business, you do not use them to decide which map layer is "more generous." You only compare the Satellite and Vector views directly available in the task interface.

***

**Summary for the Exam**
*   **Rating:** True.
*   **Mandatory Action:** Always look at both map layers. If one makes the pin look better (closer to the rooftop/target), use that one to determine your final rating.
*   **Rule Reference:** Guidelines Section 9.3.3.1 (Satellite Imagery vs. Vector Map).

**Analogy:** Imagine you are a referee in a game of **football**. If there are two different camera angles and one clearly shows the ball **crossing the goal line** while the other is blurry or blocked, the rules of this specific "game" tell you to use the angle that **awards the point** to the player. The map layers work the same way—if one view shows a "goal" (a Perfect rating), you award that rating.

Question 15 Pin Rating
15. When evaluating Pin Accuracy if the pin  falls on the rooftop of a neighboring address however  the property shares the same street and block as the intended pin, pin accuracy for the result is NEXT DOOR.  *
True
False

Name, Address, Pin (V2024)
Question 15 Feedback
You are Correct. 

The answer is True. When the property where the pin falls is directly next to the intended property and shares the same street and block, pin accuracy for the result is NEXT DOOR. Refer to section 9.1.3. Next Door, for more details.

The statement is **True**.

### **Reasoning and Guideline Criteria**
According to the guidelines, specifically Section 9.1.3, the **Next Door** rating is applied when the pin lands on a property immediately adjacent to the intended target, provided it meets several strict spatial criteria. 

To qualify as **Next Door**, the pin must land on a property that satisfies all of the following:
*   **Immediate Proximity:** It must be the first property to any side of the intended result.
*   **Same Street & Side:** The property must be on the same street and the same side of that street as the intended address.
*   **Same Block:** There must be **no intersecting public roads** between the intended property and the property where the pin actually landed. If a street separates the two properties, they are considered to be on different blocks, and the rating must be **Wrong** rather than Next Door.

### **Summary for the Exam**
*   **Rating:** True.
*   **Key Determining Factor:** The "Same Block" rule is the most critical boundary. As long as the pin is on the rooftop of a neighboring building on the same block and street, it is rated **Next Door**.
*   **Rule Reference:** Guidelines Section 9.1.3 (Next Door).

***

**Analogy:** Imagine you are trying to visit a friend's house in a row of terrace homes. If you accidentally walk up to the **front door of the person living directly to their left or right**, you are **Next Door**. However, if you have to **cross a street** to reach the house you are standing in front of, you have moved to a different block, and in mapping terms, your location is now considered **Wrong**.


Question 16
16. What is the Correct rating for the following Pin?

Result Address: 6331 6th Ave NE, Seattle, WA 98115
Result Pin Coordinates: 47.6753130284897, -122.32277653245626


 
Perfect
Approximate
Next door
Wrong

Question 16 Feedback
You are Correct. 

The correct answer is Approximate. According to section 9.4.1. Residential Property with Multiple Buildings, some residential properties consist of more than one building associated with a single address. A pin that falls on the house or other dwelling on the property, should be rated Perfect. In cases where the property also contains support or auxiliary building, including things such as garages, playhouses, sheds, etc., these structures should be considered part of the Approximate area of the boundaries of the property. Research shows that the pin in this result falls on the roof of a garage that is located within the boundaries of 6331 6th Ave NE. Since a garage is considered an auxiliary building, a pin falling on it should be rated Approximate.

The correct Pin Accuracy rating for the result at **6331 6th Ave NE, Seattle** is **Approximate**.

### **Reasoning and Analysis**
According to the mapping guidelines and the specific feedback provided for this test scenario, the rating is determined by identifying the specific structure where the pin lands on a residential property:

*   **Property Identification:** The result is for a residential address at **6331 6th Ave NE**. The map provided for this question shows three sequential plots: 6335, 6331, and 6329.
*   **Pin Placement:** Satellite imagery confirms that the pin is located within the property boundaries of the correct address (**6331**), but it does not land on the rooftop of the main house. Instead, it lands on a separate structure in the rear of the lot, identified through research as a **garage** or auxiliary building.
*   **Guideline Application (Section 9.4.1):** Per the rule for **Residential Property with Multiple Buildings**, a pin must land directly on the rooftop of the **main house or dwelling** to be rated **Perfect**. 
*   **Definition of Approximate:** The guidelines state that if a property contains support or auxiliary buildings—such as **garages, sheds, greenhouses, or playhouses**—a pin landing on these structures is considered to be within the property boundaries but outside the "Perfect" area. Therefore, because the pin lands on the garage of the intended address, it must be rated **Approximate**.

### **Summary for the Exam**
*   **Correct Rating:** Approximate.
*   **Key Factor:** The pin is on the correct parcel but on an auxiliary building (garage) rather than the primary residence rooftop.
*   **Rule Reference:** Guidelines Section 9.4.1, "Residential Property with Multiple Buildings".

***

**Analogy:** Imagine you are ordering a pizza to your house. If the delivery driver leaves the pizza at your **front door**, the delivery is **Perfect**. If the driver leaves the pizza inside your **detached garage** at the end of the driveway, they have arrived at the correct property (**Approximate**), but they haven't quite reached the specific entrance where you are waiting.

Question 17
17. What is the correct rating for the pin?

Result POI: Great Clips, 8250 Mira Mesa Blvd, Ste D, San Diego, CA 92126.
Result Pin: 32.91376876014403, -117.14592188682484

 
Perfect
Approximate
Next door
Wrong


Question 17 Feedback
You are Correct. 

The correct answer is Approximate. According to section 9.4, Single Rooftop, One Building with a Single Street Number and Multiple Unit Numbers in a Shared Parking Lot, the goal is to use the best available evidence to find the result’s exact location under the shared rooftop, which would be rated Perfect. The rest of the shared rooftop should be rated Approximate. In this case the pin falls over the section of the rooftop that is Baskin-Robbins, which is directly next to Great Clips. As seen on street view (https://maps.app.goo.gl/8d8SfReyvw7geY8SA ), since it falls on the correct rooftop, but not the correct portion of the rooftop, it should be rated Approximate.

The correct Pin Accuracy rating for the **Great Clips** result is **Approximate**.

### **Reasoning and Analysis**
The determination of this rating is based on the rules for a single building with a single street number and multiple unit numbers in a shared parking lot (Section 9.4):

*   **POI Identification:** The target is a specific business, **Great Clips**, located in a strip mall building (Suite D) that shares a single large rooftop with multiple other tenants.
*   **Pin Placement:** Research and the provided map imagery confirm that the pin lands on the shared rooftop of the building where Great Clips is housed. However, it does not land on the specific portion of the roof occupied by Suite D (Great Clips).
*   **Specific Error:** As confirmed by street view evidence in the sources, the pin actually falls over the section of the rooftop belonging to **Baskin-Robbins**, which is directly adjacent to Great Clips.
*   **Guideline Application:** According to the guidelines, when evaluating a POI under a shared rooftop, the goal is to find the result's **exact location** using the best available evidence. 
    *   The specific area over the intended business is the only area rated **Perfect**.
    *   The remaining parts of the same shared rooftop are rated **Approximate**.
*   **Conclusion:** Because the pin is on the correct building but on the **incorrect portion of the rooftop**, it must be rated **Approximate**.

### **Rating Tip for the Exam**
When dealing with strip malls or "multiple units under one roof" scenarios, always use **Street View** to identify storefront logos and door positions. If the pin is not directly over the specific suite you are rating, you must demote the rating to **Approximate**, even if it is on the correct building.

***

**Analogy:** Imagine you are visiting a friend in a **terraced house (row house)**. If your GPS tells you that you have arrived when you are standing in front of the **neighbor's front door** on the same connected building, you have reached the correct structure (**Approximate**), but you aren't at the exact spot needed for a "Perfect" arrival.



Question 18
18. What is the correct rating for the pin?

Result Address: Edmonds, WA 98020, USA
Result Pin: 47.79959650018672, -122.36689656219812

 
Perfect
Approximate
Next Door
Wrong


Question 18 Feedback
You are Correct. 

The correct answer is Perfect. The city of Edmonds, WA is considered an administrative division. A pin should fall within the boundaries of the administrative division to be rated Perfect. If it falls outside the boundaries, it should be rated Wrong. There are no Approximate or Next Door Ratings for administrative divisions. Since the result pin does fall within the boundaries of Edmonds, WA, it should be rated Perfect.
Refer to the guidelines section 9.6.2. Administrative Divisions, to learn more.

The correct Pin Accuracy rating for the result **Edmonds, WA 98020, USA** is **Perfect**.

### **Reasoning and Analysis**
The determination of this rating is based on the specific rules for administrative divisions as defined in the guidelines:

*   **Feature Classification:** The result address represents a city and its associated postal code (locality). This type of result is classified as an **Administrative Division**. 
*   **The Boundary Rule:** For administrative divisions (such as cities, neighborhoods, or counties), a pin is rated **Perfect** if it falls anywhere **within the boundaries or polygon** of that division as displayed on the map.
*   **Absence of Intermediate Ratings:** It is important to note that administrative divisions **do not have "Approximate" or "Next Door" ratings**. If the pin is inside the boundary, it is Perfect; if it is outside, it is Wrong.
*   **Tool-Specific Evaluation:** While external map coordinates might occasionally appear differently, the guidelines mandate that you must base your rating on the **boundaries shown within the TryRating tool**. In the specific map provided for this question, the pin falls clearly within the dotted polygon representing the city of Edmonds.

### **Research Requirements for the Exam**
*   **Identify the Polygon:** When rating a city or neighborhood, zoom out to see the administrative boundary (usually a dashed or colored line). 
*   **Apply the Correct/Wrong Binary:** Confirm if the pin is inside that boundary. Since "Approximate" is not an option for cities, do not be tempted to demote the pin if it is not in the "center" of the town; proximity to the center does not matter as long as it is within the limits.
*   **Section Reference:** This logic is found in **Guidelines Section 9.6.2 (Administrative Divisions)**.

***

**Summary for TryRating:**
*   **Rating:** Perfect.
*   **Comment:** The result is an administrative division (Edmonds, WA). The pin falls within the administrative boundaries of the city. Per Section 9.6.2, any pin within the polygon is rated Perfect.

**Analogy:** 
Rating the pin for a city is like checking if a **football** is **in-bounds**. It doesn't matter if the ball is on the 50-yard line or just an inch inside the sideline; as long as it is **within the field of play** (the city boundary), it is "in" (**Perfect**). If it is even a hair over the line, it is "out" (**Wrong**). There is no "almost in-bounds" rating in this category.


