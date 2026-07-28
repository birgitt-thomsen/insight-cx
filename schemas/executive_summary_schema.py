"""This script defines the data output schema for the executive insight
prompt."""

EXECUTIVE_SUMMARY_SCHEMA = {

    "type": "object",
    "properties": {
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
                    "description": "Dashboard color matching the customer health status."
                },
                "headline": {
                    "type": "string",
                    "description": "Executive headline summarizing overall customer health in 8–15 words."
                },
                "period_comparison": {
                    "type": "object",
                    "description": "Comparison with the previous reporting period.",
                    "properties": {
                        "trend": {
                            "type": "string",
                            "enum": [
                                "improving",
                                "declining",
                                "stable",
                                "unknown"
                            ],
                            "description": "Overall customer health trend compared with the previous reporting period."
                        },
                        "summary": {
                            "type": "string",
                            "description": "One sentence (15–30 words) explaining how customer health changed compared with the previous reporting period."
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
        "executive_summary": {
            "type": "string",
            "description": "Executive overview of the current customer experience in approximately 80–120 words."
        },
        "business_impact": {
            "type": "string",
            "description": "Business-focused explanation of the operational or commercial impact in approximately 40–70 words."
        },
        "top_themes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "theme": {
                        "type": "string",
                        "description": "Name of the customer feedback theme."
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of customer feedback records assigned to this theme."
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "High",
                            "Medium",
                            "Low"
                        ],
                        "description": "Business priority based on customer impact rather than frequency."
                    },
                    "insight": {
                        "type": "string",
                        "description": "Business insight explaining why this theme matters in approximately 20–35 words."
                    },
                    "period_comparison": {
                        "type": "object",
                        "description": "Comparison with the previous reporting period.",
                        "properties": {
                            "trend": {
                                "type": "string",
                                "enum": [
                                    "up",
                                    "down",
                                    "stable",
                                    "new",
                                    "unknown"
                                ],
                                "description": "Whether this theme increased, decreased, remained stable or is new compared with the previous reporting period."
                            },
                            "summary": {
                                "type": "string",
                                "description": "One sentence (15–30 words) summarizing how this theme changed compared with the previous reporting period."
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
                    "theme",
                    "count",
                    "priority",
                    "insight",
                    "period_comparison"
                ],
                "additionalProperties": False
            }
        },
        "sentiment_summary": {
            "type": "object",
            "properties": {
                "overall": {
                    "type": "string",
                    "description": "Overall sentiment classification."
                },
                "positive_percentage": {
                    "type": "number",
                    "description": "Percentage of positive feedback."
                },
                "mixed_percentage": {
                    "type": "number",
                    "description": "Percentage of mixed or neutral feedback."
                },
                "negative_percentage": {
                    "type": "number",
                    "description": "Percentage of negative feedback."
                },
                "insight": {
                    "type": "string",
                    "description": "Business interpretation of the sentiment distribution in approximately 20–35 words."
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
        "emotion_summary": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "emotion": {
                        "type": "string",
                        "description": "Name of the customer emotion."
                    },
                    "percentage": {
                        "type": "number",
                        "description": "Percentage of feedback items expressing this emotion."
                    },
                    "business_meaning": {
                        "type": "string",
                        "description": "Business interpretation of why this emotion matters in approximately 15–30 words."
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
        "leadership_priorities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Short title describing the leadership priority."
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "High",
                            "Medium",
                            "Low"
                        ],
                        "description": "Business priority level."
                    },
                    "rationale": {
                        "type": "string",
                        "description": "Business justification in approximately 20–40 words explaining why leadership should prioritize this issue."
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
        "recommended_actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Short action title."
                    },
                    "details": {
                        "type": "string",
                        "description": "Specific recommended action in approximately 30–60 words."
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "High",
                            "Medium",
                            "Low"
                        ],
                        "description": "Business priority level."
                    },
                    "owner": {
                        "type": "string",
                        "description": "Business function responsible for implementing the action."
                    },
                    "timeframe": {
                        "type": "string",
                        "description": "Recommended implementation timeframe."
                    },
                    "expected_outcome": {
                        "type": "string",
                        "description": "Expected business or customer outcome in approximately 15–30 words."
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
        "likely_root_causes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "root_cause": {
                        "type": "string",
                        "description": "Likely underlying business cause described in one concise sentence of approximately 10–20 words."
                    }
                },
                "required": [
                    "root_cause"
                ],
                "additionalProperties": False
            }
        },
        "customer_verbatims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "theme": {
                        "type": "string",
                        "description": "Theme supported by this customer comment."
                    },
                    "comment": {
                        "type": "string",
                        "description": "Original customer comment copied verbatim without summarizing or rewriting."
                    }
                },
                "required": [
                    "theme",
                    "comment"
                ],
                "additionalProperties": False
            }
        },
        "nps_insight": {
            "type": "object",
            "properties": {
                "interpretation": {
                    "type": "string",
                    "description": "Business interpretation of the NPS distribution in approximately 25–40 words."
                },
                "recommended_follow_up": {
                    "type": "string",
                    "description": "Recommended next step based on the NPS results in one concise sentence."
                },
                "promoter_percentage": {
                    "type": "number",
                    "description": "Percentage of Promoters."
                },
                "passive_percentage": {
                    "type": "number",
                    "description": "Percentage of Passives."
                },
                "detractor_percentage": {
                    "type": "number",
                    "description": "Percentage of Detractors."
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
        "csat_insight": {
            "type": "object",
            "properties": {
                "interpretation": {
                    "type": "string",
                    "description": "Business interpretation of the CSAT distribution in approximately 25–40 words."
                },
                "recommended_follow_up": {
                    "type": "string",
                    "description": "Business interpretation of the CSAT distribution in approximately 25–40 words."
                },
                "satisfied_percentage": {
                    "type": "number",
                    "description": "Percentage of satisfied customers."
                },
                "neutral_percentage": {
                    "type": "number",
                    "description": "Percentage of neutral customers."
                },
                "dissatisfied_percentage": {
                    "type": "number",
                    "description": "Percentage of dissatisfied customers."
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
        "confidence": {
            "type": "object",
            "properties": {
                "level": {
                    "type": "string",
                    "description": "Overall confidence level for the executive summary."
                },
                "score": {
                    "type": "number",
                    "description": "Confidence score between 0 and 100."
                },
                "reason": {
                    "type": "string",
                    "description": "Brief explanation in approximately 20–35 words describing why this confidence level was assigned."
                }
            },
            "required": [
                "level",
                "score",
                "reason"
            ],
            "additionalProperties": False
        },
        "key_metrics": {
            "type": "object",
            "properties": {
                "feedback_count": {
                    "type": "integer",
                    "description": "Count of feedback items."
                }
            },
            "required": [
                "feedback_count"
            ],
            "additionalProperties": False
        },
    },
    "required": [
        "customer_health",
        "executive_summary",
        "business_impact",
        "top_themes",
        "sentiment_summary",
        "emotion_summary",
        "leadership_priorities",
        "recommended_actions",
        "likely_root_causes",
        "customer_verbatims",
        "nps_insight",
        "csat_insight",
        "confidence",
        "key_metrics"
    ],
    "additionalProperties": False
}