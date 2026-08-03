"""This script defines the data output schema for the executive insight
prompt."""

EXECUTIVE_SUMMARY_SCHEMA = {

    "type": "object",
    "properties": {
        # CUSTOMER HEALTH
        "customer_health": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": [
                        "Healthy",
                        "At Risk",
                        "Critical"
                    ],
                    "description": "Overall customer health classification."
                },
                "color": {
                    "type": "string",
                    "enum": [
                        "green",
                        "amber",
                        "red"
                    ],
                    "description": (
                        "Dashboard color matching the customer health status."
                    )
                },
                "headline": {
                    "type": "string",
                    "description": (
                        "Executive headline summarizing overall "
                        "customer health in 8–15 words."
                    )
                },
                "period_comparison": {
                    "type": "object",
                    "description": (
                        "Comparison with the previous reporting period."
                    ),
                    "properties": {
                        "trend": {
                            "type": "string",
                            "enum": [
                                "improving",
                                "declining",
                                "stable",
                                "unknown"
                            ],
                            "description": (
                                "Overall customer health trend "
                                "compared with the previous reporting period."
                            )
                        },
                        "summary": {
                            "type": "string",
                            "description": (
                                "One sentence (15–30 words) explaining how "
                                "customer health changed compared with the "
                                "previous reporting period."
                            )
                        }
                    },
                    "required": [
                        "trend",
                        "summary"
                    ],
                    "additionalProperties": False
                }
            },
            "required": [
                "status",
                "color",
                "headline",
                "period_comparison"
            ],
            "additionalProperties": False
        },
        # EXECUTIVE SUMMARY
        "executive_summary": {
            "type": "string",
            "description": (
                "Executive overview of the current customer "
                "experience in approximately 80–120 words."
            )
        },
        # BUSINESS IMPACT
        "business_impact": {
            "type": "string",
            "description": (
                "Business-focused explanation of the operational or commercial "
                "impact in approximately 40–70 words."
            )
        },
        # TOP THEMES
        "top_business_drivers": {
            "type": "array",
            "description": (
                "Summarize the most important business drivers identified from "
                "primary reason codes. Focus on customer issues that have the "
                "greatest operational or commercial impact."
            ),
            "items": {
                "type": "object",
                "properties": {
                    "driver": {
                        "type": "string",
                        "description": (
                            "The primary business driver or reason code "
                            "representing a recurring customer issue or "
                            "positive experience."
                        )
                    },

                    "count": {
                        "type": "integer",
                        "description": (
                            "The number of customer feedback responses primarily "
                            "associated with this business driver."
                        )
                    },

                    "insight": {
                        "type": "string",
                        "description": (
                            "Summarize what customers are consistently saying "
                            "about this business driver and why it is significant."
                        )
                    },

                    "driver_impact": {
                        "type": "string",
                        "description": (
                            "Explain how this business driver affects customer "
                            "satisfaction, loyalty, operational performance, "
                            "revenue, costs, or business risk."
                        )
                    },

                    "period_comparison": {
                        "type": "object",
                        "description": (
                            "Compare this business driver with the previous "
                            "reporting period and explain whether its importance has changed."
                        ),
                        "properties": {
                            "trend": {
                                "type": "string",
                                "description": (
                                    "Indicate how this business driver has changed "
                                    "compared with the previous period."
                                ),
                                "enum": [
                                    "up",
                                    "down",
                                    "stable",
                                    "new"
                                ]
                            },
                            "summary": {
                                "type": "string",
                                "description": (
                                    "Briefly explain the change in frequency or "
                                    "business importance since the previous reporting period."
                                )
                            }
                        },
                        "required": [
                            "trend",
                            "summary"
                        ],
                        "additionalProperties": False
                    }
                },
                "required": [
                    "driver",
                    "count",
                    "insight",
                    "driver_impact",
                    "period_comparison"
                ],
                "additionalProperties": False
            }
        },
        # SENTIMENT SUMMARY
        "sentiment_summary": {
            "type": "object",
            "properties": {
                "overall": {
                    "type": "string",
                    "description": (
                        "Overall sentiment classification."
                    )
                },
                "positive_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of positive feedback."
                    )
                },
                "mixed_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of mixed or neutral feedback."
                    )
                },
                "negative_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of negative feedback."
                    )
                },
                "insight": {
                    "type": "string",
                    "description": (
                        "Business interpretation of the sentiment distribution "
                        "in approximately 20–35 words."
                    )
                }
            },
            "required": [
                "overall",
                "positive_percentage",
                "mixed_percentage",
                "negative_percentage",
                "insight",
                ],
                "additionalProperties": False
        },
        # EMOTION SUMMARY
        "emotion_summary": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "emotion": {
                        "type": "string",
                        "description": (
                            "Name of the customer emotion."
                        )
                    },
                    "percentage": {
                        "type": "number",
                        "description": (
                            "Percentage of feedback items expressing this "
                            "emotion."
                        )
                    },
                    "business_meaning": {
                        "type": "string",
                        "description": (
                            "Business interpretation of why this emotion "
                            "matters in approximately 15–30 words."
                        )
                    }
                },
                "required": [
                    "emotion",
                    "percentage",
                    "business_meaning",
                ],
                "additionalProperties": False
            }
        },
        # LEADERSHIP PRIORITIES
        "leadership_priorities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": (
                            "Short title describing the leadership priority."
                        )
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "High",
                            "Medium",
                            "Low"
                        ],
                        "description": (
                            "Business priority level."
                        )
                    },
                    "rationale": {
                        "type": "string",
                        "description": (
                            "Business justification in approximately "
                            "20–40 words explaining why leadership should "
                            "prioritize this issue."
                        )
                    }
                },
                "required": [
                    "title",
                    "priority",
                    "rationale",
                ],
                "additionalProperties": False
            }
        },
        # RECOMMENDED ACTIONS
        "recommended_actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": (
                            "Short action title."
                        )
                    },
                    "details": {
                        "type": "string",
                        "description": (
                            "Specific recommended action in approximately "
                            "30–60 words."
                        )
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "High",
                            "Medium",
                            "Low"
                        ],
                        "description": (
                            "Business priority level."
                        )
                    },
                    "owner": {
                        "type": "string",
                        "description": (
                            "Business function responsible for implementing "
                            "the action."
                        )
                    },
                    "timeframe": {
                        "type": "string",
                        "description": (
                            "Recommended implementation timeframe."
                        )
                    },
                    "expected_outcome": {
                        "type": "string",
                        "description": (
                            "Expected business or customer outcome in "
                            "approximately 15–30 words."
                        )
                    }
                },
                "required": [
                    "action",
                    "details",
                    "priority",
                    "owner",
                    "timeframe",
                    "expected_outcome"
                ],
                "additionalProperties": False
            }
        },
        # AI INVESTIGATION
        "ai_investigation": {
            "type": "array",
            "description": (
                "Return the 2-3 strongest AI-derived business hypotheses."
                "Order by business importance, with the highest impact hypothesis first."
            ),
            "items": {
                "type": "object",
                "properties": {
                    "hypothesis": {
                        "type": "string",
                        "description": (
                            "Short title (2-5 words) naming the underlying business issue."
                        )
                    },
                    "confidence": {
                        "type": "object",
                        "description": (
                            "The AI's confidence in this hypothesis."
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
                                    "Confidence category."
                                )
                            },
                            "score": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100,
                                "description": (
                                    "Confidence score from 0-100."
                                )
                            }
                        },
                        "required": [
                            "level",
                            "score"
                        ],
                        "additionalProperties": False
                    },
                    "summary": {
                        "type": "string",
                        "description": (
                            "One concise sentence (15-25 words) explaining why this "
                            "hypothesis matters to the business."
                        )
                    },
                    "evidence": {
                        "type": "array",
                        "description": (
                            "Return 3-5 short evidence statements supporting the hypothesis. "
                            "Each statement should be 6-12 words and reference observed "
                            "customer feedback patterns."
                        ),
                        "items": {
                            "type": "string"
                        },
                        "minItems": 3,
                        "maxItems": 5
                    },
                    "business_risk": {
                        "type": "string",
                        "description": (
                            "One concise sentence (12-20 words) describing the likely "
                            "business consequence if the issue continues."
                        )
                    },
                    "recommended_validation": {
                        "type": "string",
                        "description": (
                            "One concise sentence (8-15 words) suggesting what team, "
                            "process or operational data should be reviewed to confirm "
                            "this hypothesis."
                        )
                    }
                },
                "required": [
                    "hypothesis",
                    "confidence",
                    "summary",
                    "evidence",
                    "business_risk",
                    "recommended_validation"
                ],
                "additionalProperties": False
            },
            "minItems": 2,
            "maxItems": 3
        },
        # CUSTOMER VERBATIMS
        "customer_verbatims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "theme": {
                        "type": "string",
                        "description": (
                            "Theme supported by this customer comment."
                        )
                    },
                    "comment": {
                        "type": "string",
                        "description": (
                            "Original customer comment copied verbatim "
                            "without summarizing or rewriting."
                        )
                    }
                },
                "required": [
                    "theme",
                    "comment"
                ],
                "additionalProperties": False
            }
        },
        # NPS INSIGHT
        "nps_insight": {
            "type": "object",
            "properties": {
                "interpretation": {
                    "type": "string",
                    "description": (
                        "Business interpretation of the NPS "
                        "distribution in approximately 25–40 words."
                    )
                },
                "recommended_follow_up": {
                    "type": "string",
                    "description": (
                        "Recommended next step based on the NPS "
                        "results in one concise sentence."
                    )
                },
                "promoter_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of Promoters."
                    )
                },
                "passive_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of Passives."
                    )
                },
                "detractor_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of Detractors."
                    )
                }
            },
            "required": [
                "interpretation",
                "recommended_follow_up",
                "promoter_percentage",
                "passive_percentage",
                "detractor_percentage"
            ],
            "additionalProperties": False
        },
        # CSAT INSIGHT
        "csat_insight": {
            "type": "object",
            "properties": {
                "interpretation": {
                    "type": "string",
                    "description": (
                        "Business interpretation of the CSAT "
                        "distribution in approximately 25–40 words."
                    )
                },
                "recommended_follow_up": {
                    "type": "string",
                    "description": (
                        "Business interpretation of the CSAT "
                        "distribution in approximately 25–40 words."
                    )
                },
                "satisfied_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of satisfied customers."
                    )
                },
                "neutral_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of neutral customers."
                    )
                },
                "dissatisfied_percentage": {
                    "type": "number",
                    "description": (
                        "Percentage of dissatisfied customers."
                    )
                }
            },
            "required": [
                "interpretation",
                "recommended_follow_up",
                "satisfied_percentage",
                "neutral_percentage",
                "dissatisfied_percentage"
            ],
            "additionalProperties": False
        },
        # CONFIDENCE
        "confidence": {
            "type": "object",
            "properties": {
                "level": {
                    "type": "string",
                    "description": (
                        "Overall confidence level for the executive summary."
                    )
                },
                "score": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "description": (
                        "Confidence score between 0 and 100."
                    )
                },
                "reason": {
                    "type": "string",
                    "description": (
                        "Brief explanation in approximately "
                        "20–35 words describing why this confidence level was "
                        "assigned."
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
        # KEY METRICS
        "key_metrics": {
            "type": "object",
            "properties": {
                "feedback_count": {
                    "type": "integer",
                    "description": (
                        "Count of feedback items."
                    )
                }
            },
            "required": [
                "feedback_count"
            ],
            "additionalProperties": False
        },
        "emerging_business_risks": {
            "type": "array",
            "description": (
                "Identify the most important emerging business risks based on "
                "recurring reason codes, customer intent, emotions, sentiment "
                "and business signals. Focus on risks leadership should "
                "proactively monitor."
            ),
            "items": {
                "type": "object",
                "properties": {
                    "signal_type": {
                        "type": "string",
                        "description": (
                            "Classify the business signal as a "
                            "risk, opportunity, or emerging trend."
                        ),
                        "enum": [
                            "Risk",
                            "Opportunity",
                            "Trend"
                        ]
                    },
                    "risk": {
                        "type": "string",
                        "description": (
                            "A short title describing the identified business "
                            "signal or issue."
                        )
                    },
                    "severity": {
                        "type": "string",
                        "description": ("Assess the potential business "
                                        "impact if the signal continues or is "
                                        "not addressed."
                        ),
                        "enum": [
                            "High",
                            "Medium",
                            "Low"
                        ]
                    },
                    "likelihood": {
                        "type": "string",
                        "description": (
                            "Estimate how likely the signal is to persist or "
                            "grow based on the available customer feedback."
                        ),
                        "enum": [
                            "Increasing",
                            "Stable",
                            "Emerging",
                            "Declining"
                        ]
                    },
                    "description": {
                        "type": "string",
                        "description": (
                            "Explain the business signal, why it matters, and "
                            "the underlying customer feedback patterns "
                            "driving it."
                        ),
                    },
                    "leading_indicators": {
                        "type": "array",
                        "description": (
                            "List the key customer behaviors, reason codes, "
                            "emotions, intents, or feedback patterns that support "
                            "this business signal."
                        ),
                        "items": {
                            "type": "string"
                        }
                    },
                    "recommended_monitoring": {
                        "type": "string",
                        "description": (
                        "Recommend the metrics, operational indicators, or "
                        "customer feedback trends leadership should monitor to "
                        "validate or track this business signal over time."
                        )
                    }
                },
                "required": [
                    "signal_type",
                    "risk",
                    "severity",
                    "likelihood",
                    "description",
                    "leading_indicators",
                    "recommended_monitoring"
                ],

                "additionalProperties": False
            },
        },
        "intent_summary": {
            "type": "object",
            "description": (
                "Summarize the dominant customer intentions expressed across "
                "the analyzed feedback and explain what they indicate about "
                "future customer behavior."
            ),
            "properties": {
                "headline": {
                    "type": "string",
                     "description": (
                         "A concise executive headline summarizing the "
                         "overall customer intent landscape."
                     )
                },
                "insight": {
                    "type": "string",
                    "description": (
                        "Explain the most important customer intentions, the "
                        "underlying drivers, and their potential business implications."
                    )
                },
                "top_intents": {
                    "type": "array",
                    "description": (
                        "List the most common customer intents identified in "
                        "the analyzed feedback."
                    ),
                    "items": {
                        "type": "object",
                        "properties": {
                            "intent": {
                                "type": "string",
                                "description": (
                                    "The customer intent category identified "
                                    "from the feedback."
                                ),
                            },
                            "percentage": {
                                "type": "number",
                                "description": (
                                    "Percentage of analyzed feedback expressing "
                                    "this customer intent."
                                )
                            },
                            "business_meaning": {
                                "type": "string",
                                "description": (
                                    "Explain what this customer intent indicates "
                                    "about customer behavior and why it matters "
                                    "for the business."
                                )
                            }
                        },
                        "required": [
                            "intent",
                            "percentage",
                            "business_meaning"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": [
                "headline",
                "insight",
                "top_intents"
            ],
            "additionalProperties": False
        }
    },
    "required": [
        "customer_health",
        "executive_summary",
        "business_impact",
        "top_business_drivers",
        "sentiment_summary",
        "emotion_summary",
        "leadership_priorities",
        "recommended_actions",
        "ai_investigation",
        "customer_verbatims",
        "nps_insight",
        "csat_insight",
        "confidence",
        "key_metrics",
        "emerging_business_risks",
        "intent_summary",
    ],
    "additionalProperties": False
}