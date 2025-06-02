import pandas as pd

results = []

for row_context in range(df_context.shape[0]):
    config_values = prepare_config(df_context, row_context)
    for row_message in range(messages.shape[0]):
        message = messages['message'][row_message]
        
        # With context
        response = classify_hs(
            message=message,
            protected_characteristics_str=config_values['protected_characteristics_str'],
            HS_definition=HS_definition,
            examples=hs_examples_str,
            chain_ot=chain_ot_str,
            verbose=verbose_switch,
            community_context=config_values['community_context'],
            languages=config_values['languages'],
            geography=config_values['geography'],
            safeguarding_focus=config_values['safeguarding_focus']
        )
        result_with_context = response.choices[0].message.content

        # Without context
        response = classify_hs(
            message=message,
            protected_characteristics_str='',
            HS_definition=HS_definition,
            examples=hs_examples_str,
            chain_ot=chain_ot_str,
            verbose=verbose_switch,
            community_context='',
            languages='',
            geography='',
            safeguarding_focus=''
        )
        result_no_context = response.choices[0].message.content

        # No context, examples, or chain of thought
        response = classify_hs(
            message=message,
            protected_characteristics_str='',
            HS_definition=HS_definition,
            examples=[],
            chain_ot=[],
            verbose=verbose_switch,
            community_context='',
            languages='',
            geography='',
            safeguarding_focus=''
        )
        result_no_context_no_examples = response.choices[0].message.content

        results.append({
            'Organisation_context': config_values.get('community_context', ''),
            'Geography': config_values.get('geography', ''),
            'Languages_used': config_values.get('languages', ''),
            'Safeguarding_focus': config_values.get('safeguarding_focus', ''),
            'Protected_characteristics': config_values.get('protected_characteristics_str', ''),
            'Message': message,
            'Result_with_context': result_with_context,
            'Result_no_context': result_no_context,
            'Result_no_context_no_examples': result_no_context_no_examples
        })

# Create DataFrame and save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv("classification_results.csv", index=False)