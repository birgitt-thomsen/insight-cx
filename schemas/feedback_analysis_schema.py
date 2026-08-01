
FEEDBACK_ANALYSIS_SCHEMA = {

    "type": "object",
    "properties": {

        "sentiment": {
            "type": "string",
            "enum": [
                "Positive",
                "Neutral",
                "Negative"
            ],
            "description": (
                "Overall customer sentiment. "
                "Choose the single best matching sentiment."
            )
        },

        "emotions": {
            "type": "array",
            "description": (
                "One or two dominant customer emotions. "
                "Only include emotions that are clearly supported by the feedback."
            ),
            "items": {
                "type": "string",
                "enum": [
                    "Delighted",
                    "Confident",
                    "Appreciated",
                    "Frustrated",
                    "Disappointed",
                    "Confused",
                    "Concerned",
                    "Impatient",
                    "Angry"
                ]
            }
        },

        "intent": {
            "type": "array",
            "description": (
				"The customer's primary intention, desired outcome, "
				"or stated future behavior based on their feedback."
                "Customer actions or intentions explicitly stated or strongly implied. "
                "Return 'Unknown' when no intent can be determined."
            ),
            "items": {

                "type": "string",
                "enum": [
                  "Praise & Advocacy",
			      "Recommendation Intent",
			      "Repurchase Intent",
			      "Information Request",
			      "Support Request",
			      "Problem Resolution",
			      "Return Request",
			      "Refund Request",
			      "Replacement Request",
			      "Cancellation Request",
			      "Complaint Without Resolution Request",
			      "Escalation Request",
			      "Competitor Switch Intent",
			      "Churn Risk",
			      "Undecided",
			      "Unknown"
                ]
            }
        },

        "reason_codes": {
            "type": "array",
            "description": (
                "Ranked business reason codes explaining why the customer feels this way. "
                "Return one to three codes ordered from primary to secondary importance."
            ),
            "items": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "enum": [
							"Product - Comfort",
							"Product - Durability",
							"Product - Design",
							"Product - Size & Fit",
							"Product - Materials",
							"Product - Value",
							"Product - Availability",
							
							"Product Condition - Damaged",
							"Product Condition - Defective",
							"Product Condition - Missing Parts",
							"Product Condition - Manufacturing Quality",
							
							"Ordering - Website Experience",
							"Ordering - Product Information",
							"Ordering - Checkout",
							"Ordering - Account",
							
							"Pricing - Promotion",
							"Pricing - Discount",
							"Pricing - Price Match",
							"Pricing - Unexpected Charges",
							
							"Delivery - Speed",
							"Delivery - Scheduling",
							"Delivery - Communication",
							"Delivery - Tracking",
							"Delivery - Accuracy",
							"Delivery - Condition",
							
							"Assembly - Ease of Assembly",
							"Assembly - Instructions",
							"Assembly - Installation Service",
							
							"Customer Service - Friendliness",
							"Customer Service - Knowledge",
							"Customer Service - Responsiveness",
							"Customer Service - Communication",
							"Customer Service - Resolution",
							
							"Returns - Return Process",
							"Returns - Return Shipping",
							"Returns - Return Approval",
							"Returns - Return Status",
							
							"Refunds - Refund Speed",
							"Refunds - Refund Amount",
							"Refunds - Refund Communication",
							"Refunds - Refund Method",
							
							"Warranty - Claim Process",
							"Warranty - Coverage",
							"Warranty - Replacement",
							"Warranty - Resolution",
							
							"Billing - Payment Processing",
							"Billing - Double Charge",
							"Billing - Incorrect Charge",
							"Billing - Invoice",
							"Billing - Financing",
							"Billing - Gift Card",
							
							"Brand - Overall Experience",
							"Brand - Trust",
							"Brand - Loyalty",
                        ]
                    },

                    "rank": {
                        "type": "integer",
                        "description": (
                            "Importance ranking where 1 is the primary driver."
                        )
                    }
                },

                "required": [
                    "code",
                    "rank"
                ],

                "additionalProperties": False
            }
        },

        "priority": {
            "type": "string",
            "enum": [
                "High",
                "Medium",
                "Low"
            ],
            "description": (
                "Business priority based on customer impact, severity and urgency."
            )
        },

        "confidence": {
		    "type": "object",
		    "description": (
		        "Overall confidence in the accuracy of the analysis."
		    ),
		    "properties": {
		        "level": {
		            "type": "string",
		            "enum": [
		                "High",
		                "Medium",
		                "Low"
		            ],
		            "description": (
		                "Overall confidence level."
		            )
		        },
		        "score": {
		            "type": "integer",
		            "minimum": 0,
		            "maximum": 100,
		            "description": (
		                "Numerical confidence score between 0 and 100."
		            )
		        },
		        "reason": {
		            "type": "string",
		            "description": (
		                "Explain the confidence in one short sentence (maximum 15 words). "
		                "Mention ambiguity, conflicting signals, sarcasm, or lack of context when relevant."
		            )
		        }
		    },
		    "required": [
		        "level",
		        "score",
		        "reason"
		    ],
		    "additionalProperties": False
		},
        "business_signal": {
            "type": "string",
            "description": (
                "Business interpretation of the feedback in one sentence "
                "(maximum 20 words). Focus on the operational implication rather "
                "than paraphrasing the customer. Examples: "
                "'Delivery delays increased churn risk.' "
                "'Excellent service recovery preserved customer confidence.'"
            )
        }
    },

    "required": [
        "sentiment",
        "emotions",
        "intent",
        "reason_codes",
        "priority",
        "confidence",
        "business_signal"
    ],

    "additionalProperties": False
}